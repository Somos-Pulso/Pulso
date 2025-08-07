from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re

class Professional(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, blank=True,null=True)
    phone = models.CharField(max_length=11)
    description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    REQUIRED_FIELDS = ['phone', 'email'] 
    
    def __str__(self):
        return self.username
    
    @property
    def is_doctor(self):
        if hasattr(self, 'manager'):
            return False
        if hasattr(self, 'doctor'):
            return True
        raise ValidationError("Tipo de usuário desconhecido.")
    
    @property
    def is_manager(self):
        return not self.is_doctor
    
    def clean(self):
        errors = {}
        if self.cpf: 
            if not re.fullmatch(r'\d{11}', self.cpf):
                errors['cpf'] = 'CPF deve conter exatamente 11 dígitos numéricos (sem pontos ou traços).'
            
            if not self.__cpf_valid(self.cpf):
                errors['cpf'] = 'CPF invalido.'
        if self.cpf:
            if not re.fullmatch(r'\d{10,11}', self.phone):
                errors['phone'] = 'Telefone deve conter 10 ou 11 dígitos (sem parênteses, traços ou espaços).'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password) # gambiarra sinistra mas nao sei onde faria ja que nao tem sistema de cadastra ainda
            
        super().save(*args, **kwargs)
    
    def __cpf_valid(self, cpf: str) -> bool:
        if not cpf.isdigit() or len(cpf) != 11:
            return False

        if cpf == cpf[0] * 11:
            return False

        soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        d1 = (soma1 * 10) % 11
        if d1 == 10:
            d1 = 0

        soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        d2 = (soma2 * 10) % 11
        if d2 == 10:
            d2 = 0

        return cpf[-2:] == f"{d1}{d2}"