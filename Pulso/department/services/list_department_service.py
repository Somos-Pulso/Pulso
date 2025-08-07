from department.models import Department
from accounts.models import Manager

def get_department_by_manager(user_id):
    """"
    Retorna a lista de departamentos pelo id do gestor
    """

    try:
        manager = Manager.objects.get(manager__user_id=user_id)
        return Department.objects.filter(manager=manager, active=True)
    
    except Manager.DoesNotExist:
        return []
