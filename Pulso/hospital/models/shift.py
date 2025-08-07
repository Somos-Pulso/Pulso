from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from .schedule import Schedule

class Shift(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="shifts")
    criated_at = models.DateField(auto_now_add=True)
    atualized_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'Shift on {self.date.strftime("%d/%m/%Y")} from {self.start_time.strftime("%H:%M")} to {self.end_time.strftime("%H:%M")}'
    
    @property
    def type(self):
        return "ok-event" if self.allocations.exists() else "warn-event"
    
    @property
    def professionals(self):
        """Retorna todos os Professionals alocados neste Shift."""
        from accounts.models import Professional
        return Professional.objects.filter(
            doctor__allocations__shift=self
        ).distinct()
    
    @property
    def doctors(self):
        """Retorna todos os Doctors alocados neste Shift."""
        from accounts.models import Doctor
        return Doctor.objects.filter(
            allocations__shift=self
        ).distinct()
    
    @property
    def duration(self):
        return self.end_time - self.start_time
    
    def clean(self):
        errors = {}

        if self.start_time == self.end_time:
            errors['start_time'] = 'Horário de início e fim não podem ser iguais.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('hospital:shift_view', args=[self.pk])
