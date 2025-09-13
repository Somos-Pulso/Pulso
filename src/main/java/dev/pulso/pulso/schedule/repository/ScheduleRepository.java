package dev.pulso.pulso.schedule.repository;
import dev.pulso.pulso.schedule.model.Schedule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;

@Repository
public interface ScheduleRepository extends JpaRepository<Schedule, Long> {
    boolean existsByNameAndStartDateAndEndDateAndDepartmentId(String name, LocalDate startDate, LocalDate endDate, Long departmentId);
}
