package dev.pulso.pulso.account.repository;
import dev.pulso.pulso.account.model.Manager;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ManagerRepository  extends JpaRepository<Manager, Long>{
    Manager findByProfessionalId(Long professionalId);
}
