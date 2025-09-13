package dev.pulso.pulso.schedule.dto;

import dev.pulso.pulso.schedule.model.enums.AllocationStatus;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

public record ScheduleShiftsDTO(
        Long id,
        LocalDate date,
        LocalTime startTime,
        LocalTime endTime,
        String description,
        String type,
        List<AllocationDTO> allocations
) {
    public record AllocationDTO(
            Long id,
            String doctorPhoto,
            String doctorName,
            Boolean isConflicted,
            AllocationStatus status
    ) {}
}

