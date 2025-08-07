from django.urls import path
from .views import (
    ScheduleDetailView, ScheduleListView, CreateScheduleView ,PublishScheduleView,
    CreateShiftView, DeleteShiftView, UpdateShiftView, DeleteScheduleView, ListShiftView, DetailShift
) 

app_name = "hospital"

urlpatterns = [
    # ----------------------------------------Schedules-----------------------------------------#
    
    path("schedules/", ScheduleListView.as_view(), name="schedule_list"),
    path("schedules/create/", CreateScheduleView.as_view(), name="schedule_create"),
    path("schedules/filter/", ScheduleListView.as_view(), name='schedule_filter'),
    path("schedules/<int:pk>/", ScheduleDetailView.as_view(), name="schedule_detail"),
    path("schedules/<int:pk>/delete/", DeleteScheduleView.as_view(), name="schedule_delete"),
    path("schedules/<int:pk>/publish/", PublishScheduleView.as_view(), name="schedule_publish" ),

    # ------------------------------------------Shifts-------------------------------------------# 

    path("shifts/create/", CreateShiftView.as_view(), name="shift_create"),
    path("shifts/", ListShiftView.as_view(), name="shift_list"),
    path("shifts/<int:pk>", DetailShift.as_view(), name="shift_view"),
    path("shifts/<int:pk>/update/", UpdateShiftView.as_view(), name="shift_update"),
    path("shifts/<int:pk>/delete/", DeleteShiftView.as_view(), name="shift_delete")

]