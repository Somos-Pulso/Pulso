package dev.pulso.pulso.notification.service;

import dev.pulso.pulso.account.model.Professional;
import dev.pulso.pulso.notification.model.Notification;
import dev.pulso.pulso.notification.repository.NotificationRepository;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.*;

@Service
public class NotificationService {

    private final NotificationRepository notificationRepository;

    @Autowired
    public NotificationService(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    public Notification getNotificationById(Long id) {
        return notificationRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Notificação não encontrada"));
    }

    @Transactional
    public Notification getAndMarkAsRead(Long id, Long userId) {
        Notification notification = notificationRepository.findById(id)
                .orElse(null);

        if (notification != null && !notification.isRead()) {
            notification.setRead(true);
            notificationRepository.save(notification);
        }
        return notification;
    }

    @Transactional
    public void createNotification(Professional sender,
                                   Collection<Professional> recipients,
                                   Object targetObject,
                                   String message,
                                   String url) {

        validateSender(sender);
        List<Professional> recipientList = normalizeRecipients(recipients);

        String targetType = null;
        Long targetId = null;

        if (targetObject != null) {
            targetType = targetObject.getClass().getSimpleName();
            try {
                var pkField = targetObject.getClass().getDeclaredField("id");
                pkField.setAccessible(true);
                targetId = (Long) pkField.get(targetObject);
            } catch (NoSuchFieldException | IllegalAccessException e) {
                throw new IllegalArgumentException("Objeto alvo não possui campo id acessível");
            }
        }

        String resolvedMessage = message != null ? message : String.valueOf(targetObject);
        String resolvedUrl = url != null ? url : null; // Pode chamar método getAbsoluteUrl se quiser

        for (Professional recipient : recipientList) {
            Notification notif = new Notification();
            notif.setSender(sender);
            notif.setRecipient(recipient);
            notif.setMessage(resolvedMessage);
            notif.setTargetType(targetType);
            notif.setTargetId(targetId);
            notif.setUrl(resolvedUrl);
            notif.setCreatedAt(LocalDateTime.now());
            notif.setRead(false);
            notificationRepository.save(notif);
        }
    }

    private List<Professional> normalizeRecipients(Collection<Professional> recipients) {
        if (recipients == null || recipients.isEmpty()) {
            throw new IllegalArgumentException("Recipients não pode ser vazio");
        }
        for (Professional u : recipients) {
            if (u == null) {
                throw new IllegalArgumentException("Recipient inválido");
            }
        }
        return new ArrayList<>(recipients);
    }

    private void validateSender(Professional sender) {
        if (sender == null) {
            throw new IllegalArgumentException("Sender inválido");
        }
    }

    @Transactional
    public void markAsRead(Notification notification) {
        if (!notification.isRead()) {
            notification.setRead(true);
            notificationRepository.save(notification);
        }
    }

    public List<Notification> getProfessionalNotifications(Professional user) {
        return notificationRepository.findByRecipientOrderByCreatedAtDesc(user);
    }

    public List<Notification> getUnreadNotifications(Professional user) {
        return notificationRepository.findByRecipientAndIsReadFalseOrderByCreatedAtDesc(user);
    }

    public boolean isRead(Notification notification) {
        return notification.isRead();
    }

    public String getUrl(Notification notification) {
        if (notification.getUrl() != null) {
            return notification.getUrl();
        }
        // Se quiser implementar algo parecido com get_absolute_url
        return null;
    }

    public List<Map<String, Object>> serializeNotifications(Professional user, int limit) {
        List<Notification> unread = getUnreadNotifications(user);
        List<Map<String, Object>> result = new ArrayList<>();

        unread.stream().limit(limit).forEach(n -> {
            String msg = n.getMessage() != null ? n.getMessage() : "";
            if (msg.length() > 35) {
                msg = msg.substring(0, 35) + "...";
            }
            Map<String, Object> dto = new HashMap<>();
            dto.put("id", n.getId());
            dto.put("message", msg);
            dto.put("url", getUrl(n) != null ? getUrl(n) : "/notifications/" + n.getId() + "/detail/");
            dto.put("created_at", formatTime(n.getCreatedAt()));
            result.add(dto);
        });

        return result;
    }

    private String formatTime(LocalDateTime createdAt) {
        Duration diff = Duration.between(createdAt, LocalDateTime.now());

        if (diff.toMinutes() < 1) {
            return "agora mesmo";
        } else if (diff.toHours() < 1) {
            long minutes = diff.toMinutes();
            return "há " + minutes + " minuto" + (minutes > 1 ? "s" : "");
        } else if (diff.toHours() < 24) {
            long hours = diff.toHours();
            return "há " + hours + " hora" + (hours > 1 ? "s" : "");
        } else if (diff.toDays() == 1) {
            return "ontem às " + createdAt.toLocalTime().toString();
        } else if (diff.toDays() <= 3) {
            return "há " + diff.toDays() + " dias";
        } else {
            String[] meses = {
                    "Janeiro", "Fevereiro", "Março", "Abril",
                    "Maio", "Junho", "Julho", "Agosto",
                    "Setembro", "Outubro", "Novembro", "Dezembro"
            };
            return createdAt.getDayOfMonth() + " de " + meses[createdAt.getMonthValue() - 1];
        }
    }
}
