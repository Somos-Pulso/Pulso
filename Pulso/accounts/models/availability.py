from django.db import models
from .doctor import Doctor
from .enum import Weekday, ShiftPeriod

class Availability(models.Model):
    day = models.CharField(max_length=10, choices=Weekday.choices)
    shift = models.CharField(max_length=10, choices=ShiftPeriod.choices)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['doctor', 'day', 'shift'], name='unique_doctor_day_shift')
        ]

    def __str__(self):
        return f"{self.doctor.professional.name} - {self.day} ({self.shift})"