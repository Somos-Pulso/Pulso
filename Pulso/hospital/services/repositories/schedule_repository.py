from hospital.models import Schedule
from pulso.logger import logger


class ScheduleRepository:
    def get_schedule_or_fail(self, schedule_id: int) -> Schedule:
        try:
            return Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            logger.warning(f"Escala não encontrada: id={schedule_id}")
            raise ValueError("Escala não encontrada.")
