package dev.pulso.pulso.notification.repository;

import dev.pulso.pulso.notification.model.Notification;
import dev.pulso.pulso.account.model.Professional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, Long> {

    List<Notification> findAllByOrderByCreatedAtDesc();

    List<Notification> findByRecipientOrderByCreatedAtDesc(Professional recipient);

    List<Notification> findByRecipientAndIsReadFalseOrderByCreatedAtDesc(Professional recipient);
}