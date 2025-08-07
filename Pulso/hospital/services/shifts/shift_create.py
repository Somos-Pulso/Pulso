from accounts.models import Doctor
from hospital.models import Shift, ScheduleStatus
from django.db import transaction
from pulso.logger import logger
from ..helpers import ShiftOpsHelper
from ..helpers.serializers import ShiftSerializer
from ..repositories import RepositoryUnit
from django.utils import timezone
from datetime import datetime

class CreateShiftServices:
    def __init__(self, schedule_id: int, shift_data: dict, user_id: int):
        self.repository = RepositoryUnit()
        
        self.shift_data = shift_data
        
        self.schedule = self.repository.schedules.get_schedule_or_fail(schedule_id)
        self.user = self.repository.users.get_user_or_fail(user_id)
        
        if not self.user.is_manager : raise PermissionError("Apenas gestores podem criar um plantão.")
        
        self.SCHEDULE_PUBLISHED = self.schedule.status == ScheduleStatus.PUBLISHED
        
    def new_shift(self): 
        serializer = ShiftSerializer(self.shift)
        return serializer.to_dict()
        
    @transaction.atomic
    def create_shift(self):
        """
        Cria um novo plantão na escala informada, se o usuário tiver permissão para isso.
        O plantão é adicionado à escala e os profissionais são alocados.
        """
    
        self.shift_data = ShiftOpsHelper.normalize_shift_data(self.shift_data)
        
        shift_start = self.shift_data['start_time']
        shift_date = self.shift_data['date']

        if isinstance(shift_date, datetime):
            shift_datetime = shift_date
        else:
            shift_datetime = datetime.combine(shift_date, shift_start)
            shift_datetime = timezone.make_aware(shift_datetime, timezone.get_current_timezone())

        now = timezone.now()
        
        if shift_datetime < now:
            raise ValueError("Não é possível criar um plantão com data ou horas no passado.")
        
        self.shift = Shift.objects.create(
            schedule=self.schedule,
            date=self.shift_data['date'],
            start_time=self.shift_data['start_time'],
            end_time=self.shift_data['end_time'],
            description=self.shift_data.get('description', '')
        )
        if self.shift_data.get("allocations"):
            self._alocate_doctors_to_shift()
        else: 
            logger.warning(f"Nenhuma alocação fornecida para o plantão {self.shift.id} na escala {self.schedule.id}.")
        
    def _alocate_doctors_to_shift(self):
        """ Aloca médicos ao plantão criado. """
        
        allocations = self.shift_data.get("allocations")
        for allocation in allocations:
            doctor = Doctor.objects.get(id=allocation['doctor_id'])
            
            ShiftOpsHelper.create_allocation(
                doctor = doctor,
                shift = self.shift
            )
