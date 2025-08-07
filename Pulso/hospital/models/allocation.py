from django.db import models
from django.urls import reverse

from accounts.models.doctor import Doctor
from .enum import AllocationStatus, AllocationType

class Allocation(models.Model):
    type = models.CharField(max_length=20, choices=AllocationType.choices)
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=AllocationStatus.choices)
    shift = models.ForeignKey('Shift', on_delete=models.CASCADE, related_name='allocations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='allocations')
    criated_at = models.DateField(auto_now_add=True)
    atualized_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.doctor.professional.username} - {self.shift.date} - {self.type}"
    
    def get_absolute_url(self):
        return reverse('hostpital:shift_view', args=[self.shift.pk])