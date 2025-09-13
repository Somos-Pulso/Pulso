package dev.pulso.pulso.schedule.dto;
import dev.pulso.pulso.schedule.model.enums.ScheduleStatus;

import java.time.LocalDate;

public record DetailScheduleDTO(
        Long scheduleId,
        String name,
        LocalDate startDate,
        LocalDate endDate,
        ScheduleStatus status,
        Long departmentId,
        Long numAllAllocations,
        Long numUnallocatedShifts
) {}