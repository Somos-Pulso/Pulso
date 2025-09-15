package dev.pulso.pulso.schedule.repository;
import dev.pulso.pulso.schedule.model.Schedule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;

@Repository
public interface ScheduleRepository extends JpaRepository<Schedule, Long> {
    boolean existsByNameAndStartDateAndEndDateAndDepartmentId(String name, LocalDate startDate, LocalDate endDate, Long departmentId);

    @Query("""
        SELECT d.manager.professional.username
        FROM Schedule s
        JOIN s.department d
        WHERE s.id = :scheduleId
    """)
    String getScheduleManagerName(@Param("scheduleId") Long scheduleId);
}
