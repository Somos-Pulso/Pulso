
from .schedule_repository import ScheduleRepository
from .users_repository import UsersRepository
from .shift_repository import ShiftRepository

class RepositoryUnit:
    def __init__(self):
        self.users = UsersRepository()
        self.shifts = ShiftRepository()
        self.schedules = ScheduleRepository()
