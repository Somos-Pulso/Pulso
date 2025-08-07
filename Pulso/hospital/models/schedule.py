from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from department.models.department import Department
from .enum import ScheduleStatus
from datetime import date
import re
from django.utils.timezone import now

class Schedule(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=ScheduleStatus.choices)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='schedules')
    criated_at = models.DateField(auto_now_add=True)
    atualized_at = models.DateField(auto_now=True)
    
    def sort_schedules(schedules):
        status_order = {
            ScheduleStatus.DRAFT: 0,
            ScheduleStatus.PUBLISHED: 1,
            ScheduleStatus.ARCHIVED: 2,
        }
        return sorted(
            schedules,
            key=lambda s: (status_order.get(s.status, 99), -s.start_date.toordinal())
        )

    class Meta:
        unique_together = ('name', 'start_date', 'end_date', 'department')

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"
    
    def clean(self):
        errors = {}

        letras = re.findall(r'[A-Za-zÀ-ÿ]', self.name)
        if len(letras) < 3:
            errors['name'] = 'Nome deve conter no mínimo 3 letras.'

        today = now().date()
        min_date = today
        max_date = date(2100, 12, 31) 

        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                errors['start_date'] = 'Data de início não pode ser posterior à data de término.'

            if not (min_date <= self.start_date <= max_date):
                errors['start_date'] = 'Data de início deve estar entre hoje e 31/12/2100.'

            if not (min_date <= self.end_date <= max_date):
                errors['end_date'] = 'Data de término deve estar entre hoje e 31/12/2100.'

        conflicting = Schedule.objects.filter(
            department=self.department,
            start_date=self.start_date,
            end_date=self.end_date,
        ).exclude(pk=self.pk).exists()

        if conflicting:
            errors['__all__'] = 'Já existe uma escala com a mesma data de início e fim neste setor.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('hospital:schedule_detail', args=[str(self.id)])
    
    @property
    def professionals(self):
        from accounts.models import Professional
        return Professional.objects.filter(
            doctor__allocations__shift__schedule=self
        ).distinct()
