from django.db import models
from django.core.exceptions import ValidationError
from .professional import Professional
from department.models import Department
from datetime import time, datetime, timedelta
import re

class Doctor(models.Model):
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name='doctor')
    crm = models.CharField(max_length=20, unique=True)
    workload = models.DurationField()
    departments = models.ManyToManyField(Department, blank=True, related_name='doctors')
    specialties = models.ManyToManyField('Specialty')

    def __str__(self):
        return f"ID: {self.professional.id} - Dr. {self.professional.username} - CRM: {self.crm}"
    
    @property
    def is_fully_booked(self) -> bool:
        """Retorna True se o médico já atingiu ou excedeu sua carga horária."""
        return self.workhours >= self.workload
    
    @property
    def workhours(self) -> timedelta:
        total = timedelta()

        now = datetime.now()
        current_year = now.year
        current_month = now.month

        alocs_mes = self.allocations.select_related('shift').filter(
            shift__date__year=current_year,
            shift__date__month=current_month
        )

        for aloc in alocs_mes:
            shift = aloc.shift
            start = datetime.combine(shift.date, shift.start_time)
            end = datetime.combine(shift.date, shift.end_time)
            total += end - start

        return total

    def clean(self):
        errors = {}

        crm_pattern = r'^\d{4,6}(/(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO))?$'
        if not re.fullmatch(crm_pattern, self.crm):
            errors['crm'] = 'Formato de CRM inválido. Use até 6 dígitos, opcionalmente seguidos de /UF (ex: 123456/SP).'

        if self.workload > timedelta(hours=744):
                errors['workload'] = 'Carga horária não pode ultrapassar 744 horas mensais.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)