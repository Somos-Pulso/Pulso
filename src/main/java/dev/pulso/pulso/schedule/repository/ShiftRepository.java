package dev.pulso.pulso.schedule.repository;

import dev.pulso.pulso.schedule.model.Shift;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;


@Repository
public interface ShiftRepository extends JpaRepository<Shift, Long> {

    @Query("SELECT COUNT(sh) FROM Shift sh LEFT JOIN sh.allocations a WHERE sh.schedule.id = :scheduleId AND a.id IS NULL")
    Long countUnallocatedShifts(@Param("scheduleId") Long scheduleId);

    @Transactional
    @Query("""
        SELECT s FROM Shift s
        LEFT JOIN FETCH s.allocations a
        LEFT JOIN FETCH a.doctor d
        LEFT JOIN FETCH d.professional p
        WHERE s.schedule.id = :scheduleId
    """)
    List<Shift> findShiftsWithAllocationsAndDoctorsByScheduleId(@Param("scheduleId") Long scheduleId);

    @Transactional
    List<Shift> findByScheduleId(long id);

}
