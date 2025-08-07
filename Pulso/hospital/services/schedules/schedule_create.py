from department.models import Department
from accounts.models import Manager
from hospital.models import Schedule
from hospital.models.enum import ScheduleStatus  
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from pulso.logger import logger

class CreateSheduleService:

    @staticmethod
    def get_departments_by_user_id(user_id):
        try:
            manager = Manager.objects.get(professional_id=user_id)
            departments = Department.objects.filter(manager=manager, active=True)
            return departments
        except Manager.DoesNotExist:
            return []

    @staticmethod
    def create_schedule(name, start_date, end_date, department_id):
        try:
            nome_formatado = name.strip()

            exists = Schedule.objects.filter(
                name=nome_formatado,
                start_date=start_date,
                end_date=end_date,
                department_id=department_id
            ).exists()

            if exists:
                raise ValidationError("Já existe uma escala com essas informações.")

            new_schedule = Schedule.objects.create(
                name=nome_formatado,
                start_date=start_date,
                end_date=end_date,
                status=ScheduleStatus.DRAFT,  
                department_id=department_id
            )

            return new_schedule

        except IntegrityError:
            raise ValidationError("Já existe uma escala com essas informações.")

        except ValidationError:
            raise 

        except Exception as e:
            raise Exception(f"Erro inesperado ao criar escala: {str(e)}")
