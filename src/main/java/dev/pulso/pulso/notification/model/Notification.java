package dev.pulso.pulso.notification.model;

import dev.pulso.pulso.account.model.Professional;
import jakarta.persistence.*;
import jakarta.validation.constraints.Size;
import java.time.LocalDateTime;

@Entity
@Table(name = "notifications")
public class Notification {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "TEXT")
    private String message;

    @ManyToOne
    @JoinColumn(name = "sender_id")
    private Professional sender;

    @ManyToOne
    @JoinColumn(name = "recipient_id")
    private Professional recipient;

    @Column(nullable = false)
    private boolean isRead = false;

    // Simula GenericForeignKey
    @Column(name = "target_type")
    private String targetType;  // exemplo: "allocation", "shift"

    @Column(name = "target_id")
    private Long targetId;      // id do objeto relacionado

    @Column
    private String url;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    // Construtores
    public Notification() {}

    public Notification(String message, Professional sender, Professional recipient) {
        this.message = message;
        this.sender = sender;
        this.recipient = recipient;
    }

    // Getters e setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public Professional getSender() { return sender; }
    public void setSender(Professional sender) { this.sender = sender; }

    public Professional getRecipient() { return recipient; }
    public void setRecipient(Professional recipient) { this.recipient = recipient; }

    public boolean isRead() { return isRead; }
    public void setRead(boolean read) { isRead = read; }

    public String getTargetType() { return targetType; }
    public void setTargetType(String targetType) { this.targetType = targetType; }

    public Long getTargetId() { return targetId; }
    public void setTargetId(Long targetId) { this.targetId = targetId; }

    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    // Métodos auxiliares
    public void markAsRead() {
        this.isRead = true;
    }

    public String getTargetUrl() {
        if (this.url != null) {
            return this.url;
        }
        // Em Java, não existe GenericForeignKey automático
        // Você precisaria implementar lógica para buscar o objeto pelo tipo e ID
        return null;
    }

    public String typeName() {
        return targetType != null ? targetType.toLowerCase() : "default";
    }

    @Override
    public String toString() {
        String msgPreview = message != null && message.length() > 50 ? message.substring(0, 50) : message;
        return "Notification (" + createdAt + ") - " + msgPreview;
    }
}
