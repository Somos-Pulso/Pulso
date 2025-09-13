package dev.pulso.pulso.schedule.repository;

import dev.pulso.pulso.schedule.model.Shift;
import dev.pulso.pulso.schedule.projection.ScheduleShiftProjection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ShiftRepository extends JpaRepository<Shift, Long> {

    @Query("SELECT COUNT(sh) FROM Shift sh LEFT JOIN sh.allocations a WHERE sh.schedule.id = :scheduleId AND a.id IS NULL")
    Long countUnallocatedShifts(@Param("scheduleId") Long scheduleId);

    @Query("""
            SELECT s.id AS id,
                   s.date AS date,
                   s.startTime AS startTime,
                   s.endTime AS endTime,
                   s.description AS description,
                   a.id AS allocations_id,
                   a.status AS allocations_status,
                   CASE\s
                       WHEN EXISTS (
                           SELECT 1 FROM Allocation a2
                           WHERE a2.doctor.id = a.doctor.id
                             AND a2.shift.date = s.date
                             AND a2.shift.startTime < s.endTime
                             AND a2.shift.endTime > s.startTime
                             AND a2.id <> a.id
                             AND a2.shift.schedule.department.id <> s.schedule.department.id
                       ) THEN true
                       ELSE false
                   END AS allocations_isConflicted,
                   d.professional.username AS allocations_doctor_username,
                   d.professional.profilePicture AS allocations_doctor_profilePicture
            FROM Shift s
            JOIN s.allocations a
            JOIN a.doctor d
            WHERE s.schedule.id = :scheduleId
           \s""")
    List<ScheduleShiftProjection> findShiftsBySchedule(@Param("scheduleId") Long scheduleId);

}
