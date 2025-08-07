from django.db import models
from django.core.exceptions import ValidationError
# from accounts.models import Manager
import re

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    manager = models.ForeignKey("accounts.Manager", on_delete=models.SET_NULL, null=True, blank=True, related_name='departments')

    def clean(self):
        errors = {}

        if not re.match(r'^[A-Za-z0-9\s]+$', self.name):
            errors['name'] = ('O nome deve conter apenas letras, números e espaços.')

        if errors:
            raise ValidationError(errors)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
