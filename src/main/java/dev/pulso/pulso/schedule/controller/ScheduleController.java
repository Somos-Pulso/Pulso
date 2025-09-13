package dev.pulso.pulso.schedule.controller;

import dev.pulso.pulso.schedule.dto.DetailScheduleDTO;
import dev.pulso.pulso.schedule.dto.ScheduleRequestDTO;
import dev.pulso.pulso.schedule.dto.ScheduleShiftsDTO;
import dev.pulso.pulso.schedule.model.Schedule;
import dev.pulso.pulso.schedule.service.schedule.CreateScheduleService;
import dev.pulso.pulso.exception.ScheduleAlreadyExistsException;
import dev.pulso.pulso.exception.DepartmentNotFoundException;
import dev.pulso.pulso.schedule.service.schedule.DetailScheduleService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/schedules")
public class ScheduleController {

    private final CreateScheduleService createScheduleService;
    private final DetailScheduleService detailService;

    public ScheduleController(CreateScheduleService createService, DetailScheduleService detailService) {
        this.createScheduleService = createService;
        this.detailService = detailService;
    }

    @GetMapping("/detail")
    public ResponseEntity<DetailScheduleDTO> getSchedule(@RequestBody ScheduleRequestDTO request) {
        DetailScheduleDTO dto = detailService.getSchedule(request.scheduleId(), request.userId());
        return ResponseEntity.ok(dto);
    }

    @GetMapping("/{scheduleId}/shifts")
    public ResponseEntity<List<ScheduleShiftsDTO>> getShiftsBySchedule(@PathVariable long scheduleId) {
        List<ScheduleShiftsDTO> shifts = detailService.getShiftsBySchedule(scheduleId);
        if (shifts.isEmpty()) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.ok(shifts);
    }

    @PostMapping
    public ResponseEntity<?> createSchedule(@RequestBody Map<String, String> body) {
        try {
            String name = body.get("name");
            LocalDate startDate = LocalDate.parse(body.get("startDate"));
            LocalDate endDate = LocalDate.parse(body.get("endDate"));
            Long departmentId = Long.parseLong(body.get("departmentId"));

            Schedule schedule = createScheduleService.createSchedule(name, startDate, endDate, departmentId);

            return ResponseEntity.status(HttpStatus.CREATED).body(schedule);

        } catch (ScheduleAlreadyExistsException ex) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(Map.of("error", ex.getMessage()));

        } catch (DepartmentNotFoundException ex) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("error", ex.getMessage()));

        } catch (Exception ex) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Erro inesperado ao criar escala: " + ex.getMessage()));
        }
    }
}
