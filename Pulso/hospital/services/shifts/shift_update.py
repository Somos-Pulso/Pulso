from django.db import transaction
from accounts.models import Doctor
from hospital.models import Allocation, ScheduleStatus

from notification.services import NotificationService
from ..helpers import ShiftOpsHelper
from ..helpers.serializers import ShiftSerializer
from pulso.logger import logger
from ..repositories import RepositoryUnit

class UpdateShiftServices:
    def __init__(self, shift_id: int, shift_data: dict, user_id: int):
        self.repository = RepositoryUnit()
        
        self.shift_data = shift_data
        logger.debug(self.shift_data)
        self.shift = self.repository.shifts.get_shift_or_fail(shift_id)
        self.user = self.repository.users.get_user_or_fail(user_id)
        
        if not self.user.is_manager : raise PermissionError("Medicos não tem permissão para atulizar plantões")
        
        self.schedule_status = self.shift.schedule.status
        self.current_allocations = self.shift.allocations.select_related("doctor").all()
        self.removed_doctors = []
        self.SHIFT_EDITABLE_FIELDS = ("date", "start_time", "end_time", "description")

    def updated_shift(self):
        serializer = ShiftSerializer(self.shift)
        return serializer.to_dict()
        
    @transaction.atomic
    def update_shift(self):
        """
        Atualiza um plantão existente. Pode alterar data, horários, descrição e alocações.
        A atualização de alocações é feita comparando as antigas com as novas:
            - Alocações removidas são deletadas.
            - Novas alocações são criadas.
            - Alocações existentes são mantidas.
        """
        self.shift_data = ShiftOpsHelper.normalize_shift_data(self.shift_data)
        was_published = self.schedule_status == ScheduleStatus.PUBLISHED
        
        for field in self.SHIFT_EDITABLE_FIELDS:
            if field in self.shift_data:
                setattr(self.shift, field, self.shift_data[field])
        self.shift.save()
        
        self._sync_allocations()
        
        if was_published : 
            notification_service = NotificationService()
            notification_service.create_notification(
                sender = self.user, 
                recipients = self.shift.professionals, 
                target_object = self.shift,
                message = f"Plantão atualizado para {self.shift.date}, no departamento {self.shift.schedule.department}.", 
            )
        else: logger.info(f"Nenhuma nova notificação ao atualizar o plantão {self.shift.id}")
        
        logger.info(f"Plantão {self.shift.id} atualizado com sucesso por {self.user.username}.")

    def _sync_allocations(self):
        """ Sincroniza alocações atualizadas com as salvas no banco de dados """
        new_allocations = self.shift_data.get('allocations', [])
        current_allocations = self.current_allocations
        current_ids = {a.doctor.id for a in current_allocations}
        new_ids = {a['doctor_id'] for a in new_allocations}

        self._remove_outdated_allocations(current_ids, new_ids)
        self._add_new_allocations(current_ids, new_allocations)

    def _remove_outdated_allocations(self, current_ids : list[int], new_ids : list[int]):
        """ Remove do banco de dados alocações apagadas e guarda em uma variavel os medicos removidos """
        to_remove = list(set(current_ids) - set(new_ids))
        if to_remove:
            self.removed_doctors = Doctor.objects.filter(id__in=to_remove)
            Allocation.objects.filter(shift=self.shift, doctor_id__in=to_remove).delete()
            
    def _add_new_allocations(self, current_ids : list, new_allocations : list):
        """ Adiciona novas alocações no plantão """
        for data in new_allocations:
            doc_id = data['doctor_id']
            if doc_id not in current_ids:
                doctor = Doctor.objects.get(id=doc_id)
                ShiftOpsHelper.create_allocation(
                    doctor = doctor,
                    shift = self.shift
                )

                    
 
                          
