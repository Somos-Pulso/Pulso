from notification.services import NotificationService
from accounts.models import Professional
from hospital.models import Schedule, Allocation
from pulso.logger import logger
from django.core.exceptions import ValidationError
from django.db import transaction
from hospital.models import AllocationType, ScheduleStatus
from ..repositories import RepositoryUnit

class PublishScheduleService:
    def __init__(self, schedule_id : int, user_id : int):
        self.repository = RepositoryUnit()
        self.user = self.repository.users.get_user_or_fail(user_id)
        self.schedule = self.repository.schedules.get_schedule_or_fail(schedule_id)
        if not self.user.is_manager : raise PermissionError("Médicos não tem permissão para publicar escala")
        
    @transaction.atomic
    def publish_schedule(self):
        """
        Publica a escala informada, se o usuário tiver permissão para isso.
        A escala é marcada como publicada e os profissionais são notificados.
        """
        
        if not self.schedule.shifts.exists(): raise ValueError("não é possivel publicar escalas sem plantões")
        
        match self.schedule.status:
            case ScheduleStatus.DRAFT:
                self.schedule.status = ScheduleStatus.PUBLISHED
                self.schedule.save()

                if self.schedule.professionals.exists():
                    notification_service = NotificationService()
                    notification_service.create_notification(
                        sender = self.user, 
                        recipients = self.schedule.professionals, 
                        target_object = self.schedule,
                        message = f"Nova escala publicada no departamento {self.schedule.department}, você pode ter novos plantões atribuidos.", 
                    )
            case ScheduleStatus.PUBLISHED:
                raise ValueError("Não é possivel publicar uma escala ja publicada")
            case ScheduleStatus.ARCHIVED:
                raise ValidationError("Não é possivel publicar uma escala arquivada")
        logger.info(f"Escala {self.schedule.id} publicada com sucesso por {self.user.username}.")
