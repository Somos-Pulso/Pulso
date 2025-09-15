package dev.pulso.pulso.schedule.service.schedule;

import dev.pulso.pulso.schedule.dto.DetailScheduleDTO;
import dev.pulso.pulso.schedule.dto.ScheduleShiftDTO;
import dev.pulso.pulso.schedule.model.Allocation;
import dev.pulso.pulso.schedule.model.Schedule;
import dev.pulso.pulso.schedule.model.Shift;
import dev.pulso.pulso.schedule.repository.AllocationRepository;
import dev.pulso.pulso.schedule.repository.ScheduleRepository;
import dev.pulso.pulso.schedule.repository.ShiftRepository;
import dev.pulso.pulso.helper.ShiftHelper;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


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

    public List<ScheduleShiftDTO> getShiftsBySchedule(long scheduleId){
        List<Shift> shifts = shiftRepo.findShiftsWithAllocationsAndDoctorsByScheduleId(scheduleId);
        String scheduleManager = scheduleRepo.getScheduleManagerName(scheduleId);
        Map<Long, Boolean> conflicts = getAllocationConflicts(shifts);


        return shifts.stream()
                .map(shift -> new ScheduleShiftDTO(
                        shift.getId(),
                        shift.getDate(),
                        shift.getStartTime(),
                        shift.getEndTime(),
                        shift.getDescription(),
                        ShiftHelper.getShiftType(shift.getDate(), shift.getEndTime(), shift.getAllocations()),
                        scheduleManager,
                        shift.getAllocations().stream()
                                .map(allocation -> new ScheduleShiftDTO.AllocationDTO(
                                        allocation.getId(),
                                        allocation.getDoctor().getProfessional().getProfilePicture(),
                                        allocation.getDoctor().getProfessional().getUsername(),
                                        conflicts.get(allocation.getId()),
                                        allocation.getStatus()
                                ))
                                .toList()
                ))
                .toList();
    }

    private Map<Long, Boolean> getAllocationConflicts(List<Shift> shifts){
        List<Long> allocationIds = shifts.stream()
                .flatMap(s -> s.getAllocations().stream())
                .map(Allocation::getId)
                .toList();

        return allocationRepo.findConflicts(allocationIds).stream()
                .collect(Collectors.toMap(
                        row -> (Long) row[0],
                        row -> (Boolean) row[1]
                ));
    }
}
