from hospital.models import Shift
from pulso.logger import logger


class ShiftRepository:
    def get_shift_or_fail(self, shift_id: int) -> Shift:
        try:
            return Shift.objects.select_related("schedule").get(id=shift_id)
        except Shift.DoesNotExist:
            logger.warning(f"Plantão não encontrado: id={shift_id}")
            raise ValueError("Plantão não encontrado.")
