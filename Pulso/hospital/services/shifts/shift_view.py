from hospital.models import Shift
from accounts.models import Doctor


class ShiftViewService():
    
    @classmethod
    def get_shift(cls, shift_id: int):
        shift = Shift.objects.get(id=shift_id)

        doctors = Doctor.objects.filter(allocations__shift=shift).prefetch_related("specialties").distinct()

        for doctor in doctors:
            doctor.first_specialty = doctor.specialties.first().name if doctor.specialties.exists() else "Sem especialidade"

        return {
            'shift': shift,
            'doctors': doctors
        }
