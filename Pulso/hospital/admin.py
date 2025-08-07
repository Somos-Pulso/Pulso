from django.contrib import admin
from .models import Allocation, Schedule, Shift

admin.site.register(Allocation)
admin.site.register(Schedule)
admin.site.register(Shift)