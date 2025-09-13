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
        SELECT CASE WHEN COUNT(a2) > 0 THEN true ELSE false END
        FROM Allocation a2
        WHERE a2.doctor = :#{#allocation.doctor}
          AND a2.shift.date = :#{#allocation.shift.date}
          AND a2.shift.startTime < :#{#allocation.shift.endTime}
          AND a2.shift.endTime > :#{#allocation.shift.startTime}
          AND a2 <> :allocation
          AND a2.shift.schedule.department <> :#{#allocation.shift.schedule.department}
    """)
    boolean existsConflict(@Param("allocation") Allocation allocation);
}
