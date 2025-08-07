from accounts.models import Doctor
from department.models import Department
from hospital.models import Shift
from django.views import View

class ShiftListService(View):
    
    @classmethod
    def get_user_shifts(cls, user_id: int, dept=None):
        doctor = Doctor.objects.get(professional_id=user_id)
        departments = Department.objects.filter(doctors=doctor)
        
        shifts = Shift.objects.filter(allocations__doctor=doctor).select_related('schedule__department')
        
        if dept and dept != 'everything':
            shifts = shifts.filter(schedule__department__id=int(dept))
        
        return {
            'shifts': shifts,
            'doctor': doctor,
            'departments': departments,
            'selected_dept': dept,
            'is_doctor': True,
        }