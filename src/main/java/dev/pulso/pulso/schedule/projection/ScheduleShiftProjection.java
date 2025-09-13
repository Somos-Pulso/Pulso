package dev.pulso.pulso.schedule.projection;

import java.time.LocalDate;
import java.util.List;
import java.time.LocalTime;

public interface ScheduleShiftProjection {
    Long getId();
    LocalDate getDate();
    LocalTime getStartTime();
    LocalTime getEndTime();
    String getDescription();
    List<AllocationProjection> getAllocations();

    interface AllocationProjection {
        Long getId();
        String getStatus();
        Boolean getIsConflicted(); // Já calculado no banco
        DoctorInfo getDoctor();

        interface DoctorInfo {
            String getUsername();
            String getProfilePicture();
        }
    }
}

