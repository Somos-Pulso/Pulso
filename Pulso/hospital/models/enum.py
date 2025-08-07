from django.db import models

class ScheduleStatus(models.TextChoices):
    PUBLISHED = "Publicado", "Published"
    DRAFT = "Rascunho", "Draft"
    ARCHIVED = "Arquivado", "Archived"

class AllocationType(models.TextChoices):
    SUGGESTED = "Sugestão", "Suggested"
    DIRECT = "Direta", "Direct"

class AllocationStatus(models.TextChoices):
    CONFIRMED = "Confirmada", "Confirmed"
    REJECTED = "Recusada", "Rejected"
    PENDING = "Em Aberto", "Pending"