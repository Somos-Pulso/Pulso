package dev.pulso.pulso.schedule.controller;

import dev.pulso.pulso.schedule.dto.ScheduleShiftsDTO;
import dev.pulso.pulso.schedule.dto.ShiftSaveRequestDTO;
import dev.pulso.pulso.schedule.service.shift.SaveShiftService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/shift")
public class ShiftController {
    private final SaveShiftService saveService;

    public ShiftController(SaveShiftService saveSvr){
        this.saveService = saveSvr;
    }

    @PostMapping("/save")
    public ResponseEntity<ScheduleShiftsDTO> save(@RequestBody @Valid ShiftSaveRequestDTO request) {
        ScheduleShiftsDTO shift = saveService.save(request);
        return ResponseEntity.ok(shift);
    }

}
