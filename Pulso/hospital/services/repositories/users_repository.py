from accounts.models import Professional
from department.models import Department
from accounts.models import Doctor
from pulso.logger import logger

class UsersRepository:
    def get_user_or_fail(self, user_id: int) -> Professional:
        try:
            return Professional.objects.get(id=user_id)
        except Professional.DoesNotExist:
            logger.security(f"Usuário não encontrado: id={user_id}")
            raise PermissionError("Usuário não encontrado.")
        
    def get_department_doctors(self, department: Department):
        if not isinstance(department, Department):
            raise ValueError(f"Esperado Department, recebeu {type(department).__name__}")

        doctors = (
            Doctor.objects
            .filter(departments=department)
            .select_related("professional")
            .prefetch_related("specialties")
            .distinct()
        )
        if not doctors.exists():
            logger.warning(f"Nenhum médico encontrado no departamento {department.name}")
        return doctors