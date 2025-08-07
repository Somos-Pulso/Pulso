from django.db import models
from hospital.models import Allocation
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from accounts.models import Professional as User


class Notification(models.Model):
    message = models.TextField(help_text="Texto da notificação.", blank=True, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_notifications",
        help_text="Usuário que gerou a notificação."
    )
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="received_notifications",
        help_text="Usuário que recebeu a notificação."
    )
    is_read = models.BooleanField(default=False, help_text="Indica se a notificação foi lida.")

    # Generic relationship to associate the notification with any object (e.g. scale, shift, etc. it was only allocation before)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True, 
        help_text="Tipo do objeto relacionado à notificação."
    )
    object_id = models.PositiveIntegerField(null=True, blank=True,
        help_text="ID do objeto relacionado à notificação."
    )
    content_object = GenericForeignKey("content_type", "object_id")
    
    url = models.URLField(blank=True, help_text="URL para acessar objeto  associado.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Data e hora de criação.")
    
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        # Utiliza os primeiros 50 caracteres da mensagem para identificação
        return f"Notificação ({self.created_at:%Y-%m-%d %H:%M}) - {self.message[:50]}"
    
    def mark_as_read(self):
        """Marks the notification as read for a user."""
        self.is_read = True
    
    def get_target_url(self):
        """
        Returns the associated URL:
         - Uses the 'url' field if it is defined.
         - Otherwise, tries to call 'get_absolute_url' on the related object.
        """
        if self.url:
            return self.url
        if self.content_object and hasattr(self.content_object, 'get_absolute_url'):
            return self.content_object.get_absolute_url()
        return None
    
    def type_name(self):
        """
        Returns the name of the related object type (e.g. 'allocation', 'shift', etc.).
        Can be used in templates for conditional rendering.
        """
        if self.content_type:
            return self.content_type.model.lower()
        return "default"
    