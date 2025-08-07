from django.db import models
from .professional import Professional

class Manager(models.Model):
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name='manager')

    def __str__(self):
        return f"Manager: {self.professional.username}"