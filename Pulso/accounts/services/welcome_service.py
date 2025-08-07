from accounts.models import Professional
from department.models import Department
from hospital.models import Schedule, Allocation, Shift, enum
from notification.models import Notification
from django.utils import timezone
from django.db.models import Count
from datetime import date, timedelta
from django.utils.timezone import localtime

class WelcomeService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_user_welcome(self, user_id):
        try:
            user = Professional.objects.select_related("doctor", "manager").get(id=user_id)
        except Professional.DoesNotExist:
            return None

        if user.is_doctor:
            return self._make_context_doctor(user)
        else:
            return self._make_context_manager(user)
        
    def _make_context_doctor(self, professional):
        return {
            "is_doctor": professional.is_doctor,
            "professional": self._get_serialized_professional_info(professional),
            "shifts": self._get_doctor_serialized_shifts(professional),
            "notifications": self._get_doctor_serialized_notifications(professional),
        }

    def _make_context_manager(self, professional):
        return {
            "is_doctor": professional.is_doctor,
            "professional": self._get_serialized_professional_info(professional),
            "schedules": self._get_serialized_schedules(professional),
            "shifts": self._get_manager_serialized_shifts(professional),
            "statistics": self._get_serialized_statistics(professional),
            "sector_occupancy": self._get_serialized_sector_occupancy(),
        }
    
    def _get_doctor_serialized_notifications(self, professional):
        notifications = Notification.objects.filter(recipient=professional).order_by('-created_at')

        serialized = []
        for notification in notifications:
            
            message = notification.message
            if len(message) > 45:
                message = message[:45] + "..."

            sender = notification.sender
            serialized.append({
                "message": message,
                "sender_name": sender.username if sender else "Sistema",
                "sender_photo": sender.profile_picture.url if sender and sender.profile_picture else None,
                "created_at": localtime(notification.created_at).strftime("%d/%m/%Y %H:%M"),
                "url": notification.url or "#",
                "is_read": notification.is_read,
            })

        return serialized
        
    def _get_serialized_professional_info(self, professional):
        if professional.is_doctor:
            workhours_timedelta = professional.doctor.workhours
            workload_timedelta = professional.doctor.workload

            workhours = round(workhours_timedelta.total_seconds() / 3600, 2)
            workload = round(workload_timedelta.total_seconds() / 3600, 2)
            freehours = round(workload - workhours, 2)

            work_percent = round((workhours / workload) * 100) if workload else 0
            free_percent = 100 - work_percent if workload else 0

            return {
                "name": professional.username,
                "workload": workload,
                "workhours": workhours,
                "freehours": freehours,
                "work_percent": work_percent,
                "free_percent": free_percent,
            }
        else:
            return {"name": professional.username}
    
    def _get_doctor_serialized_shifts(self, professional):
        today = date.today()
        tomorrow = today + timedelta(days=1)

        shifts = Shift.objects.filter(
            allocations__doctor=professional.doctor,
            date__gte=today
        ).select_related(
            "schedule__department"
        ).distinct().order_by("date", "start_time")

        serialized = []

        for shift in shifts:
            schedule = shift.schedule
            department = schedule.department

            if shift.date == today:
                date_display = "Hoje"
            elif shift.date == tomorrow:
                date_display = "Amanhã"
            else:
                date_display = shift.date.strftime("%d/%m/%Y")

            serialized.append({
                "id": shift.id,
                "start_time": shift.start_time.strftime("%H:%M"),
                "end_time": shift.end_time.strftime("%H:%M"),
                "date": date_display,
                "manager_name": self._get_manager_name(shift),
                "department": self._shorten_department_name(department.name),
            })

        return serialized

    def _get_serialized_schedules(self, professional):
        schedules =self._get_draft_schedules(professional)

        serialized = []

        for schedule in schedules:
            formatted_date = f"{schedule.start_date.strftime('%d/%m/%Y')} - {schedule.end_date.strftime('%d/%m/%Y')}"
            
            name = schedule.name
            if len(name) > 20:
                name = name[:20] + "..."
            
            serialized.append({
                "id": schedule.id,
                "name": name,
                "formatted_date": formatted_date,
            })

        return serialized
    
    def _get_draft_schedules(self, professional):
        return Schedule.objects.filter(department__manager=professional.manager, status=enum.ScheduleStatus.DRAFT).order_by("-start_date")

    def _get_manager_serialized_shifts(self, professional):
        shifts = Shift.objects.filter(
            schedule__department__manager=professional.manager,
            schedule__status=enum.ScheduleStatus.DRAFT
        ).prefetch_related("allocations__doctor", "schedule__department__manager__professional")

        serialized = []

        for shift in shifts:
            schedule = shift.schedule
            department = schedule.department

            is_empty = not shift.allocations.exists()

            has_conflict = False
            for alloc in shift.allocations.all():
                overlapping_allocations = Allocation.objects.filter(
                    doctor=alloc.doctor,
                    shift__date=shift.date,
                    shift__start_time__lt=shift.end_time,
                    shift__end_time__gt=shift.start_time,
                ).exclude(shift__schedule__department=department)

                if overlapping_allocations.exists():
                    has_conflict = True
                    break

            if is_empty or has_conflict:
                serialized.append({
                    "id": shift.id,
                    "start_time": shift.start_time.strftime("%H:%M"),
                    "end_time": shift.end_time.strftime("%H:%M"),
                    "date": shift.date.strftime("%d/%m/%Y"),
                    "manager_name": self._get_manager_name(shift),
                    "department": self._shorten_department_name(department.name),
                    "is_empty": is_empty,
                    "has_conflict": has_conflict,
                })

        return serialized

    def _get_manager_name(self, shift):
        manager = shift.schedule.department.manager
        prof = manager.professional if manager else None
        return (
            prof.get_full_name().strip()
            or prof.username
            or prof.email
            if prof else "Desconhecido"
        )
    
    def _shorten_department_name(self, name, max_length=12):
        return name[:max_length] + "..." if len(name) > max_length else name
    
    
    def _get_serialized_statistics(self, professional):
        today = timezone.now().date()

        shifts = Shift.objects.filter(
            schedule__department__manager=professional.manager,
            date__year=today.year,
            date__month=today.month
        ).annotate(
            allocation_count=Count("allocations")
        )

        total_shifts = shifts.count()
        shifts_without_doctor = shifts.filter(allocation_count=0).count()

        doctor_ids = set()
        for shift in shifts:
            for alloc in shift.allocations.all():
                doctor_ids.add(alloc.doctor_id)

        total_doctors = len(doctor_ids)

        return {
            "total_shifts": total_shifts,
            "unallocated_shifts": shifts_without_doctor,
            "total_doctors": total_doctors,
        }

    def _get_serialized_sector_occupancy(self):
        departments = Department.objects.all()

        result = []

        for department in departments:
            total_shifts = 0
            filled_shifts = 0

            for schedule in department.schedules.all():
                for shift in schedule.shifts.all():
                    total_shifts += 1
                    if shift.allocations.exists():
                        filled_shifts += 1

            percentage = round((filled_shifts / total_shifts) * 100) if total_shifts else 0

            result.append({
                "sector": department.name,
                "filled_percentage": percentage,
            })

        result.sort(key=lambda x: x["filled_percentage"], reverse=True)
        return result[:3]