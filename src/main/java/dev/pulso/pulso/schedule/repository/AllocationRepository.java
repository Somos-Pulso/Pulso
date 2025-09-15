package dev.pulso.pulso.schedule.repository;
import dev.pulso.pulso.schedule.model.Allocation;
import dev.pulso.pulso.schedule.model.Shift;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface AllocationRepository extends JpaRepository<Allocation, Long> {

    @Query("SELECT COUNT(DISTINCT a.doctor) FROM Allocation a WHERE a.shift.schedule.id = :scheduleId")
    Long countDistinctDoctorsBySchedule(@Param("scheduleId") Long scheduleId);

    List<Allocation> findByShift(Shift shift);

    @Query("""
        SELECT a.id, CASE WHEN COUNT(a2) > 0 THEN true ELSE false END
        FROM Allocation a
        LEFT JOIN Allocation a2 ON a2.doctor = a.doctor
            AND a2.shift.date = a.shift.date
            AND a2.shift.startTime < a.shift.endTime
            AND a2.shift.endTime > a.shift.startTime
            AND a2.shift.schedule.department <> a.shift.schedule.department
            AND a2 <> a
        WHERE a.id IN :allocationIds
        GROUP BY a.id
    """)
    List<Object[]> findConflicts(@Param("allocationIds") List<Long> allocationIds);
}
