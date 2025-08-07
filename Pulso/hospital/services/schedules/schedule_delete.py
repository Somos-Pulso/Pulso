from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from pulso.logger import logger
from django.db import transaction
from ..repositories import ScheduleRepository

class ScheduleDeleteService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @transaction.atomic
    def delete_schedule(self, schedule_id):
        repository = ScheduleRepository()
        schedule = repository.get_schedule_or_fail(schedule_id)
        
        now_datetime = timezone.now()  # timezone-aware

        for shift in schedule.shifts.all():
            shift_datetime = datetime.combine(shift.date, shift.end_time)
            shift_datetime = timezone.make_aware(shift_datetime, timezone.get_current_timezone())

            if shift_datetime <= now_datetime:
                raise ValidationError("Não é possível excluir a escala: já possui plantões passados")
            
        schedule.delete()
        logger.info(f"Escala {schedule} Deletada com sucesso")