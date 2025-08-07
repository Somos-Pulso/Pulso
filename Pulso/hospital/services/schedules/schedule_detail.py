from django.db.models import Count, Q, Prefetch
from hospital.models import Schedule, Shift, Allocation
from pulso.logger import logger
from ..repositories import UsersRepository
from ..helpers.serializers import serialize_shifts_to_json, serialize_doctors_to_json


class ScheduleDetailService:
    def __init__(self, schedule_id: int, user_id: int):
        self.repository = UsersRepository()
        self.user = self.repository.get_user_or_fail(user_id)
        self.schedule = self._get_schedule_with_all_data_or_fail(schedule_id)
        self.manager = self.schedule.department.manager
        self.doctors = self.repository.get_department_doctors(self.schedule.department)
        self._annotate_counts()
        
    def schedule_data(self) -> dict:
        if self.user.is_manager:
            return self._manager_context()
        else:
            return self._regular_user_context()

    def _manager_context(self) -> dict:
        return {
            "schedule": self.schedule,
            "manager_name": self.manager.professional.username,
            "doctors": serialize_doctors_to_json(self.doctors),
            "shifts": serialize_shifts_to_json(self.schedule.shifts.all()),
            "is_doctor": False,
        }

    def _regular_user_context(self) -> dict:
        return {
            "schedule": self.schedule,
            "manager_name": self.manager.professional.username,
            "shifts": serialize_shifts_to_json(self.schedule.shifts.all()),
            "is_doctor": True,
        }

    def _get_schedule_with_all_data_or_fail(self, schedule_id: int) -> Schedule:
        allocation_queryset = Allocation.objects.select_related(
            "doctor__professional"
        ).only(
            "id", "status",
            "doctor__professional__id",
            "doctor__professional__username",
            "doctor__professional__profile_picture"
        )
        shift_queryset = Shift.objects.annotate(
            allocations_count=Count("allocations")
        ).prefetch_related(
            Prefetch("allocations", queryset=allocation_queryset)
        )

        shifts_prefetch = Prefetch("shifts", queryset=shift_queryset)

        try:
            return Schedule.objects.select_related("department").prefetch_related(
                shifts_prefetch
            ).get(id=schedule_id)
        except Schedule.DoesNotExist:
            logger.error(f"Escala com ID {schedule_id} não encontrada.")
            raise ValueError("A escala solicitada não foi encontrada")

    def _annotate_counts(self) -> None:
        counts = (
            Schedule.objects
            .filter(id=self.schedule.id)
            .annotate(
                num_all_allocations=Count('shifts__allocations__doctor', distinct=True),
                num_unallocated_shifts=Count(
                    'shifts',
                    filter=Q(shifts__allocations__isnull=True),
                    distinct=True,
                )
            )
            .values('num_all_allocations', 'num_unallocated_shifts')
            .first()
        ) or {'num_all_allocations': 0, 'num_unallocated_shifts': 0}

        self.schedule.num_all_allocations = counts['num_all_allocations']
        self.schedule.num_unallocated_shifts = counts['num_unallocated_shifts']
