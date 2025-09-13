package dev.pulso.pulso.schedule.dto;

import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

public record ShiftSaveRequestDTO(
                 Long id,
        @NotNull Long scheduleId,
        @NotNull LocalDate date,
        @NotNull LocalTime startTime,
        @NotNull LocalTime endTime,
                 String description,
                 List<Long> doctorsAllocatedId
) {
}
