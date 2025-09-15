package dev.pulso.pulso.schedule.service.shift;

import dev.pulso.pulso.account.model.Doctor;
import dev.pulso.pulso.account.repository.DoctorRepository;
import dev.pulso.pulso.helper.ShiftHelper;
import dev.pulso.pulso.schedule.dto.ScheduleShiftDTO;
import dev.pulso.pulso.schedule.dto.ShiftSaveRequestDTO;
import dev.pulso.pulso.schedule.model.Allocation;
import dev.pulso.pulso.schedule.model.Schedule;
import dev.pulso.pulso.schedule.model.Shift;
import dev.pulso.pulso.schedule.repository.AllocationRepository;
import dev.pulso.pulso.schedule.repository.ScheduleRepository;
import dev.pulso.pulso.schedule.repository.ShiftRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class SaveShiftService {
    private final ScheduleRepository scheduleRepo;
    private final ShiftRepository shiftRepo;
    private final AllocationRepository allocationRepo;
    private final DoctorRepository doctorRepo;

    public SaveShiftService(ScheduleRepository schRepo, ShiftRepository shiRepo,
                            AllocationRepository allocRepo, DoctorRepository docRepo){

        this.doctorRepo = docRepo;
        this.allocationRepo = allocRepo;
        this.shiftRepo = shiRepo;
        this.scheduleRepo = schRepo;
    }

    @Transactional
    public ScheduleShiftDTO save(ShiftSaveRequestDTO request){
        Schedule schedule = scheduleRepo.findById(request.scheduleId())
                .orElseThrow(() -> new EntityNotFoundException("Schedule not found"));

        boolean isUpdate = request.id() != null;

        if (isUpdate){
            return update(request, schedule);
        }
        return create(request, schedule);

    }
    private ScheduleShiftDTO create(ShiftSaveRequestDTO request, Schedule schedule) {

        Shift newShift = new Shift(
                request.date(),
                request.startTime(),
                request.endTime(),
                request.description(),
                schedule
        );
        shiftRepo.save(newShift);

        String scheduleManager = scheduleRepo.getScheduleManagerName(schedule.getId());
        List<Allocation> allocations = updateDoctorsToShift(newShift, request.doctorsAllocatedId());

        return makeReponse(newShift, allocations, scheduleManager);
    }

    private ScheduleShiftDTO update(ShiftSaveRequestDTO request, Schedule schedule){
        Shift shift = shiftRepo.findById(request.id())
                .orElseThrow(() -> new IllegalArgumentException("Shift not found"));

        shift.setDate(request.date());
        shift.setStartTime(request.startTime());
        shift.setEndTime(request.endTime());
        shift.setDescription(request.description());
        shiftRepo.save(shift);

        String scheduleManager = scheduleRepo.getScheduleManagerName(schedule.getId());
        List<Allocation> allocations = updateDoctorsToShift(shift, request.doctorsAllocatedId());

        return makeReponse(shift, allocations, scheduleManager);
    }


    private ScheduleShiftDTO makeReponse(Shift shift, List<Allocation> allocations, String cratedBy){
        Map<Long, Boolean> conflicts = getAllocationConflicts(allocations);
        return new ScheduleShiftDTO(
                shift.getId(),
                shift.getDate(),
                shift.getStartTime(),
                shift.getEndTime(),
                shift.getDescription(),
                ShiftHelper.getShiftType(shift.getDate(), shift.getEndTime(), allocations),
                cratedBy,
                allocations.stream()
                        .map(a -> new ScheduleShiftDTO.AllocationDTO(
                                a.getId(),
                                a.getDoctor().getProfessional().getProfilePicture(),
                                a.getDoctor().getProfessional().getUsername(),
                                conflicts.get(a.getId()),
                                a.getStatus()
                        ))
                        .toList()
        );
    }
    
    private Map<Long, Boolean> getAllocationConflicts(List<Allocation> allocations){
        List<Long> allocationIds = allocations.stream()
                .map(Allocation::getId)
                .toList();

        return allocationRepo.findConflicts(allocationIds).stream()
                .collect(Collectors.toMap(
                        row -> (Long) row[0],
                        row -> (Boolean) row[1]
                ));
    }


    private List<Allocation> updateDoctorsToShift(Shift shift, List<Long> doctorIds) {
        List<Doctor> doctors = doctorRepo.findAllById(doctorIds);
        List<Allocation> existingAllocs = allocationRepo.findByShift(shift);
        List<Allocation> finalAllocs = new ArrayList<>();

        Map<Long, Allocation> existingMap = existingAllocs.stream()
                .collect(Collectors.toMap(a -> a.getDoctor().getId(), a -> a));


        for (Doctor doctor : doctors) {
            Allocation alloc = existingMap.getOrDefault(doctor.getId(),
                    new Allocation(shift, doctor, null, null, null));
            finalAllocs.add(alloc);
        }

        List<Allocation> toRemove = existingAllocs.stream()
                .filter(a -> !doctorIds.contains(a.getDoctor().getId()))
                .toList();


        allocationRepo.deleteAll(toRemove);
        allocationRepo.saveAll(finalAllocs);
        return finalAllocs;
    }
}
