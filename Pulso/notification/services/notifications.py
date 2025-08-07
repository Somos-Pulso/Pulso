from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

from accounts.models import Professional as User
from notification.models import Notification

from django.utils.timezone import now
import datetime




class NotificationService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_notification_by_id(self, pk):
        return Notification.objects.filter(pk=pk).first()

    def get_and_mark_as_read(self, pk, user_id):
        """
        Retrieves the notification for the given user and marks it as read (if not already).
        Returns the notification or None if it does not belong to the user.
        """
        #TODO: in another moment, separate the mark_as_read function to use it for notify de sender that the notification was read
            
        notification = Notification.objects.filter(pk=pk).first()
        if notification and not notification.is_read:
            notification.is_read = True
            notification.save()
        return notification


    def create_notification(self, *, sender, recipients, target_object=None, message=None, url=None):
        """
        Creates a notification for one or more recipients.

        Parameters:
        - sender: User who triggered the notification.
        - recipients: A user or a list of users who will receive the notification.
        - target_object: An object related to the notification (any model instance).
        - message: Optional custom text for the notification (default: str(target_object)).
        - url: Optional URL to redirect to (default: target_object.get_absolute_url()).

        Note: it's important to implement `get_absolute_url()` in the related model
        if you want the notification to redirect to the object page.

        Example:
            service.create_notification(
                sender=user:User,
                recipients=[recipent1:User, recipient2:User],
                target_object=object or None,
                message="New shift available" or None,
                url=None or "app_name:detail_url" pk=object.pk"
            )

        Returns:
        - Created Notification instance.
        """
        self._validate_sender(sender)
        recipients = self._normalize_recipients(recipients)
        content_type, object_id = self._resolve_content_type(target_object)
        message, url = self._resolve_message_and_url(target_object, message, url)

        for recipient in recipients:
            Notification.objects.create(
                sender=sender,
                recipient=recipient,
                message=message,
                content_type=content_type,
                object_id=object_id,
                url=url
            )


    def _normalize_recipients(self, recipients):
        """
        Ensures recipients are a list of valid User instances.
        """
        if isinstance(recipients, User):
            recipients_list = [recipients]

        elif hasattr(recipients, '__iter__'):
            recipients_list = list(recipients)

        else:
            raise ValidationError("Recipients deve ser um User, QuerySet ou lista de Users.")

        if not recipients_list or not all(isinstance(u, User) for u in recipients_list):
            raise ValidationError("Todos os recipients devem ser instâncias de User.")

        return recipients_list

    def _validate_sender(self, sender):
        """
        Validates that the sender is a User instance.
        """
        if not isinstance(sender, User):
            raise ValidationError("Sender must be a valid User instance.")

    def _resolve_content_type(self, obj):
        """
        Returns the ContentType and object ID for the given object.
        """
        if obj:
            if not hasattr(obj, 'pk') or obj.pk is None:
                raise ValidationError("Target object must be saved (must have a primary key).")
            return ContentType.objects.get_for_model(obj), obj.pk
        return None, None

    def _resolve_message_and_url(self, target_object, message, url):
        """
        Fallback logic for message and URL when not explicitly provided.
        If not message is provided, it will be set to the string representation of the target object.
        If not URL is provided, it will be set to the get_absolute_url method of the target object.
        """
        if not message and target_object:
            message = str(target_object)

        if not url and target_object:
            url = target_object.get_absolute_url() or None
        return message, url

    def mark_as_read(self, notification: Notification):
        """
        Marks a specific notification as read by the given user.
        """
        if not self.is_read(notification):
            notification.is_read = True
            notification.save()


    def get_user_notifications(self, user):
        """
        Returns all notifications received by the user.
        """
        if user.is_superuser:
            return Notification.objects.all().order_by('-created_at')
        return Notification.objects.filter(recipient=user).order_by('-created_at')

    def get_unread_notifications(self, user):
        """
        Returns all unread notifications for the given user.
        """
        return self.get_user_notifications(user).exclude(is_read=True).order_by('-created_at')

    def is_read(self, notification: Notification) -> bool:
        """
        Checks if the given notification was already read.
        """
        return notification.is_read
    
    def get_url(self, notification: Notification):
        """
        Returns the associated URL:
        - If 'notification.url' is defined, uses it.
        - Otherwise, tries to call 'get_absolute_url()' on the related object (if it exists).
        - Otherwise, returns None.
        """
        return notification.get_target_url()
# API

    def serialize_notifications(self, user, limit=10):
        """
        Returns a serialized list of the latest unread notifications for a user.
        The return value is already formatted to be sent as JSON by the view.
        """
        notifications = self.get_unread_notifications(user)[:limit]
        result = []
        for n in notifications:
            message = n.message or ""
            if len(message) > 35:
                message = message[:35] + "..."

            result.append({
                "id": n.id,
                "message": message,
                "url": n.get_target_url() or f"/notifications/{n.id}/detail/",
                "created_at": self._format_time(n.created_at)
            })
        return result

    def _format_time(self, dt):
        """
        Converts the datetime of creation of the notification to a friendly string.

        - < 1 minute: 'agora mesmo'
        - < 1 hour: 'há X minutos'
        - < 24 hours: 'há X horas'
        - 1–2 days (24–48h): 'ontem às HH:MM'
        - 2–3 days: 'há X dias'
        - > 3 days: 'DD de Mês' (ex: 12 de Julho)
        """
        current_time = now()
        diff = current_time - dt

        if diff < datetime.timedelta(minutes=1):
            return "agora mesmo"
        elif diff < datetime.timedelta(hours=1):
            minutes = int(diff.total_seconds() // 60)
            return f"há {minutes} minuto{'s' if minutes > 1 else ''}"
        elif diff < datetime.timedelta(hours=24):
            hours = int(diff.total_seconds() // 3600)
            return f"há {hours} hora{'s' if hours > 1 else ''}"
        elif diff < datetime.timedelta(days=2):
            return f"ontem às {dt.strftime('%H:%M')}"
        elif diff < datetime.timedelta(days=4):
            days = diff.days
            return f"há {days} dias"
        else:
            meses = {
                1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
            }
            return f"{dt.day} de {meses[dt.month]}"