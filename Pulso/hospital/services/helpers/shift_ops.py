from notification.services import NotificationService
from accounts.models import Doctor
from hospital.models import Shift, Allocation, AllocationType, AllocationStatus, ScheduleStatus
from datetime import datetime, date, timedelta
from pulso.logger import logger
from dataclasses import dataclass

@dataclass(frozen=True)
class ShiftTypes:
    UNFILLED = "unfilled-shift"
    PAST = "past-shift"
    OK = "ok-shift"




class ShiftOpsHelper:
    @staticmethod
    def normalize_shift_data(shift_data : dict) -> dict:
        """ Normaliza os dados recebidos do formulário do plantão. """
        try:
            return {
                "date": datetime.strptime(shift_data["date"], "%Y-%m-%d").date(),
                "start_time": datetime.strptime(shift_data["start_time"], "%H:%M").time(),
                "end_time": datetime.strptime(shift_data["end_time"], "%H:%M").time(),
                "description": str(shift_data.get("description", "")).strip(),
                "allocations": list(shift_data.get("allocations", []))
            }

        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Erro ao normalizar shift_data: {e} | Dados: {shift_data}")
            raise ValueError("Dados de plantão ou alocação mal formatados.")

        except Exception as e:
            logger.critical(e, exc_info=True)
            raise Exception(f"Erro inesperado ao normalizar dados: {e}")
        
    @staticmethod
    def create_allocation(doctor: Doctor, shift : Shift) -> Allocation:
        """ Cria uma alocação para um médico no plantão solicitado . """

        is_direct = not doctor.is_fully_booked
        return_date = date.today() if is_direct else None
        status = AllocationStatus.CONFIRMED if is_direct else AllocationStatus.PENDING
        aloc_type = AllocationType.DIRECT if is_direct else AllocationType.SUGGESTED
        
        aloc = Allocation.objects.create(
            shift=shift,
            doctor=doctor,
            return_date=return_date,
            status=status,
            type=aloc_type
        )
        service = NotificationService()
        if shift.schedule.status == ScheduleStatus.PUBLISHED:
            if aloc.type == AllocationType.DIRECT:
                service.create_notification(
                    sender=shift.schedule.department.manager.professional,
                    recipients=[doctor.professional],
                    target_object=shift,
                    message=f"Você foi alocado para um novo plantão em {shift.date.strftime('%d/%m/%Y')}.",
                )
                logger.metric(f"Médico {doctor} alocado ao plantao {shift} na escala {shift.schedule}")
            else:
                service.create_notification(
                    sender=shift.schedule.department.manager.professional,
                    recipients=[doctor.professional],
                    target_object=shift,
                    message=f"Um novo plantão foi sugerido para você em {shift.date.strftime('%d/%m/%Y')}.",
                )
                logger.info(f"Médico {doctor} com carga horaria completa sugerido ao plantao {shift} na escala {shift.schedule}")
        
        
        return aloc
    
    @staticmethod
    def get_shift_status(shift) -> str:
        """
        Retorna o status de um plantão:
        - 'past-shift' se já passou.
        - 'unfilled-shift' se não tem médicos alocados.
        - 'ok-shift' se está válido.
        """
        now = datetime.now()

        end_datetime = datetime.combine(shift.date, shift.end_time)
        if end_datetime < now:
            return ShiftTypes.PAST

        if not shift.allocations.exists():
            return ShiftTypes.UNFILLED

        return ShiftTypes.OK
    
    @staticmethod
    def allocation_is_conflicted(allocation) -> bool:
        """
        Verifica se a alocação conflita com outro plantão do mesmo médico em outro departamento no mesmo horário.
        """
        shift = allocation.shift
        doctor = allocation.doctor

        return Allocation.objects.filter(
            doctor=doctor,
            shift__date=shift.date,
            shift__start_time__lt=shift.end_time,
            shift__end_time__gt=shift.start_time,
        ).exclude(
            id=allocation.id
        ).exclude(
            shift__schedule__department=shift.schedule.department
        ).exists()