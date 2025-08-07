from accounts.models import Professional, Manager
from department.models import Department
from hospital.models import Schedule, Allocation
from datetime import date, timedelta
from django.utils.dateformat import format as django_date_format
from pulso.logger import logger
import calendar
from django.db.models import Q

class ScheduleListService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_user_schedules(self, user_id, filters):
        try:
            user = Professional.objects.select_related("doctor", "manager").get(id=user_id)

            departments = (
                user.doctor.departments.all()
                if user.is_doctor
                else Department.objects.filter(manager=user.manager)
            )

            schedules = (
                Schedule.objects
                .filter(department__in=departments)
                .select_related("department", "department__manager", "department__manager__professional")
                .prefetch_related("shifts")
            )

            if user.is_doctor:
                try:
                    manager_instance = user.manager
                except Manager.DoesNotExist:
                    manager_instance = None

                schedules = schedules.exclude(
                    Q(status='Rascunho') & ~Q(department__manager=manager_instance)
                )

            if filters:
                period = filters.get("period")
                if period:
                    schedules = ScheduleListService.filter_schedules_by_duration(schedules, period)

                department_id = filters.get("department_id")
                if department_id:
                    schedules = schedules.filter(department_id=department_id)

                status = filters.get("status")
                if status:
                    schedules = schedules.filter(status=status)

            schedules = Schedule.sort_schedules(schedules)
            schedules = ScheduleListService._serialize_schedules(schedules)

            context = ScheduleListService._make_context(user.is_doctor, schedules, departments)
            return context

        except Professional.DoesNotExist:
            logger.error(f"Profissional com ID {user_id} não encontrado.")
            raise ValueError("Usuário não encontrado.")

        except Exception as e:
            logger.critical(f"Erro inesperado ao buscar escalas para o usuário {user_id}: {str(e)}", exc_info=True)
            raise Exception(f"Erro inesperado ao buscar escalas {str(e)}.")

    def _make_context(user_is_doctor, schedules, departments):
        return {
            "is_doctor": user_is_doctor,
            "schedules": schedules,
            "departments": departments,
        }

    def _serialize_schedules(schedules):
        serialized = []

        for schedule in schedules:

            name = schedule.name
            if len(name) > 60:
                name = name[:60] + "..."
                
            serialized.append({
                "id": schedule.id,
                "name": name,
                "start_date": schedule.start_date.isoformat(),
                "end_date": schedule.end_date.isoformat(),
                "criated_at": django_date_format(schedule.criated_at, "d/m/Y"),
                "period": f"{django_date_format(schedule.start_date, 'd/m/Y')} - {django_date_format(schedule.end_date, 'd/m/Y')}",
                "status": schedule.status,
                "num_shifts": schedule.shifts.count(),
                "num_conflicts": ScheduleListService._get_conflict_count(schedule),
                "manager_name": ScheduleListService._get_manager_name(schedule),
                "department": {
                    "id": schedule.department.id,
                    "name": schedule.department.name,
                },
            })
        
        return serialized

    def _get_conflict_count(schedule):
        conflict_count = 0

        for shift in schedule.shifts.prefetch_related("allocations__doctor"):
            for alloc in shift.allocations.select_related("doctor"):
                overllaping_alocations = Allocation.objects.filter(
                    doctor=alloc.doctor,
                    shift__date=shift.date,
                    shift__start_time__lt=shift.end_time,
                    shift__end_time__gt=shift.start_time,
                ).exclude(shift__schedule__department=schedule.department)
                
                if overllaping_alocations.exists():
                    conflict_count += 1
                    break

        return conflict_count

    def _get_manager_name(schedule):
        manager = schedule.department.manager
        prof = manager.professional if manager else None
        return (
            prof.get_full_name().strip()
            or prof.username
            or prof.email
            if prof else "Desconhecido"
        )

    def filter_schedules_by_duration(schedules, period):
        min_days, max_days = ScheduleListService._get_duration_range_for_period(period)

        if min_days is None:
            return schedules.none()

        result = []
        for schedule in schedules:
            duration = (schedule.end_date - schedule.start_date).days + 1
            if min_days <= duration <= max_days:
                result.append(schedule)

        return result

    def _get_duration_range_for_period(period):
        if period == "semanal":
            return 1, 8
        elif period == "mensal":
            return 9, 32
        elif period == "bimestral":
            return 33, 63
        elif period == "trimestral":
            return 64, 94
        elif period == "semestral":
            return 95, 187
        elif period == "anual":
            return 188, 3650
        else:
            return None, None