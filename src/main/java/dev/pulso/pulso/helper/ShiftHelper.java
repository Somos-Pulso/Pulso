package dev.pulso.pulso.helper;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

public class ShiftHelper {
    public static <T> String getShiftType(LocalDate date, LocalTime endTime, List<T> allocations) {
        LocalDateTime endDateTime = LocalDateTime.of(date, endTime);

        if (endDateTime.isBefore(LocalDateTime.now())) {
            return "past-shift";
        }
        if (allocations == null || allocations.isEmpty()) {
            return "unfilled-shift";
        }
        return "ok-shift";
    }
}
