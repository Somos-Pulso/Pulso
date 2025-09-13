package dev.pulso.pulso.hospital.repository;
import dev.pulso.pulso.hospital.model.Department;
import dev.pulso.pulso.account.model.Manager;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface DepartmentRepository extends JpaRepository<Department, Long> {
    List<Department> findByManagerAndActiveTrue(Manager manager);

}