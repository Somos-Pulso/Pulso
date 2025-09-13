package dev.pulso.pulso.helper;

import dev.pulso.pulso.schedule.projection.ScheduleShiftProjection;

import java.time.LocalDateTime;

public class ShiftHelper {
    public static String getShiftType(ScheduleShiftProjection shift) {
        LocalDateTime endDateTime = LocalDateTime.of(shift.getDate(), shift.getEndTime());

        if (endDateTime.isBefore(LocalDateTime.now())) {
            return "past-shift";
        }
        if (shift.getAllocations() == null || shift.getAllocations().isEmpty()) {
            return "unfilled-shift";
        }
        return "ok-shift";
    }
}
