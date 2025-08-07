from datetime import timedelta
from hospital.services.helpers import ShiftOpsHelper
import json
from pulso.logger import logger

class ShiftSerializer:
    def __init__(self, shift):
        self.shift = shift
        
    def to_dict(self) -> dict:
        return {
            "id": self.shift.id,
            "date": self.shift.date.isoformat(),
            "start_time": self.shift.start_time.strftime('%H:%M'),
            "end_time": self.shift.end_time.strftime('%H:%M'),
            "created_by": self.shift.schedule.department.manager.professional.username,
            "description": self.shift.description or "",
            "type" : ShiftOpsHelper.get_shift_status(self.shift),
            "allocations": [self._serialize_allocation(a) for a in self.shift.allocations.all()],
        }


    def _serialize_allocation(self, allocation) -> dict:
        doctor = allocation.doctor.professional
        return {
            "id": allocation.doctor.id,
            "photo": doctor.profile_picture.url if doctor.profile_picture else None,
            "status": allocation.status,
            "username": doctor.username,
            "is_conflicted": ShiftOpsHelper.allocation_is_conflicted(allocation)
        }



class DoctorSerializer:
    def __init__(self, doctor):
        self.doctor = doctor

    def _format_duration(self, td: timedelta) -> str:
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"

    def to_dict(self) -> dict:
        return {
            "id": self.doctor.id,
            "nome": self.doctor.professional.username,
            "especialidades": [s.name for s in self.doctor.specialties.all()],
            "foto_url": self.doctor.professional.profile_picture.url if self.doctor.professional.profile_picture else None,
            "workload": self._format_duration(self.doctor.workload),
            "workhours": self._format_duration(self.doctor.workhours),
        }

def serialize_shifts_to_json(shifts) -> str:
    return json.dumps([ShiftSerializer(s).to_dict() for s in shifts])


def serialize_doctors_to_json(doctors) -> str:
    return json.dumps([DoctorSerializer(d).to_dict() for d in doctors])