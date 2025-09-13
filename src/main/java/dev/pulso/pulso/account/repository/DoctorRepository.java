package dev.pulso.pulso.account.repository;

import dev.pulso.pulso.account.model.Doctor;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DoctorRepository extends JpaRepository<Doctor, Long> {


}
