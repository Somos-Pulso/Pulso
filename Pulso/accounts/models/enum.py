from django.db import models

class Weekday(models.TextChoices):
    MONDAY = "segunda", "Monday"
    TUESDAY = "terça", "Tuesday"
    WEDNESDAY = "quarta", "Wednesday"
    THURSDAY = "quinta", "Thursday"
    FRIDAY = "sexta", "Friday"

class ShiftPeriod(models.TextChoices):
    DAY = "dia", "Day"
    AFTERNOON = "tarde", "Afternoon"
    NIGHT = "noite", "Night"