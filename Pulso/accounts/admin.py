from django.contrib import admin
from .models import (
    Specialty, Availability,
    Professional, Doctor, Manager
)

admin.site.register(Specialty)
admin.site.register(Availability)
admin.site.register(Professional)
admin.site.register(Doctor)
admin.site.register(Manager)