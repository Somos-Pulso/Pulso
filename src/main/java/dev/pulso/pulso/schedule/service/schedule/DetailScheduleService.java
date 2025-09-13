package dev.pulso.pulso.schedule.service.schedule;

import dev.pulso.pulso.schedule.dto.DetailScheduleDTO;
import dev.pulso.pulso.schedule.dto.ScheduleShiftsDTO;
import dev.pulso.pulso.schedule.model.Schedule;
import dev.pulso.pulso.schedule.model.Shift;
import dev.pulso.pulso.schedule.repository.AllocationRepository;
import dev.pulso.pulso.schedule.repository.ScheduleRepository;
import dev.pulso.pulso.schedule.repository.ShiftRepository;
import dev.pulso.pulso.helper.ShiftHelper;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;


@Service
public class DetailScheduleService {
    private final ScheduleRepository scheduleRepo;
    private final ShiftRepository shiftRepo;
    private final AllocationRepository allocationRepo;

    public DetailScheduleService( ScheduleRepository scheduleRepo, ShiftRepository shiftRepo, AllocationRepository allocRepo){
        this.scheduleRepo = scheduleRepo;
        this.allocationRepo = allocRepo;
        this.shiftRepo = shiftRepo;
    }
    public DetailScheduleDTO getSchedule(long scheduleId){
        Schedule schedule = scheduleRepo.findById(scheduleId)
                .orElseThrow(() -> new IllegalArgumentException("Schedule not found"));
        Long numAllAllocations = allocationRepo.countDistinctDoctorsBySchedule(scheduleId);
        Long numUnallocatedShifts = shiftRepo.countUnallocatedShifts(scheduleId);

        return new DetailScheduleDTO(
                schedule.getId(),
                schedule.getName(),
                schedule.getStartDate(),
                schedule.getEndDate(),
                schedule.getStatus(),
                schedule.getDepartment().getId(),
                numAllAllocations,
                numUnallocatedShifts
        );
    };

    public List<ScheduleShiftsDTO> getShiftsBySchedule(long scheduleId){
        List<Shift> projections = shiftRepo.findShiftsWithAllocationsAndDoctorsByScheduleId(scheduleId);
        List<Shift> shifts = shiftRepo.findByScheduleId(scheduleId);

        System.out.println(shifts);
        System.out.println(projections);

        String managerName = "flavio";
        return projections.stream()
                .map(p -> new ScheduleShiftsDTO(
                        p.getId(),
                        p.getDate(),
                        p.getStartTime(),
                        p.getEndTime(),
                        p.getDescription(),
                        ShiftHelper.getShiftType(p.getDate(), p.getEndTime(), p.getAllocations()),
                        p.getAllocations().stream()
                                .map(a -> new ScheduleShiftsDTO.AllocationDTO(
                                        a.getId(),
                                        a.getDoctor().getProfessional().getProfilePicture(),
                                        a.getDoctor().getProfessional().getUsername(),
                                        allocationRepo.existsConflict(a),
                                        a.getStatus()
                                ))
                                .toList()
                ))
                .toList();
    }

}
