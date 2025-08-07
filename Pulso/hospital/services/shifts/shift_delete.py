from accounts.models import Doctor
from hospital.models import ScheduleStatus
from notification.services import NotificationService
from pulso.logger import logger
from django.db import transaction

from ..repositories import RepositoryUnit

class DeleteShiftServices:
    def __init__(self, shift_id: int, user_id: int):
        self.repository = RepositoryUnit()
        
        self.user = self.repository.users.get_user_or_fail(user_id)
        if not self.user.is_manager : raise PermissionError("Apenas administradores podem deletar um plantão.")
        
        self.shift = self.repository.shifts.get_shift_or_fail(shift_id)
        self.SCHEDULE_PUBLISHED = self.shift.schedule.status == ScheduleStatus.PUBLISHED

    @transaction.atomic
    def delete_shift(self):


        doctors_in_shift_deleted = list(
            Doctor.objects.filter(allocations__shift=self.shift).distinct()
        )
        professionals = [doctor.professional for doctor in doctors_in_shift_deleted]
        #professionals = self.shift.professionals

        self.shift.delete()

        logger.info(f"Plantão {self.shift} deletado com sucesso por {self.user.username}.")

        if self.SCHEDULE_PUBLISHED :
            notification_service = NotificationService()
            notification_service.create_notification(
                sender = self.user, 
                recipients = professionals, 
                target_object = self.shift.schedule,
                message = f"Você foi dispensado do plantão dia {self.shift.date} as {self.shift.start_time} - {self.shift.end_time} no setor {self.shift.schedule.department}", 
            )
