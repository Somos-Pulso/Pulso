package dev.pulso.pulso.schedule.service.shift;

import dev.pulso.pulso.account.model.Doctor;
import dev.pulso.pulso.account.repository.DoctorRepository;
import dev.pulso.pulso.schedule.dto.ScheduleShiftsDTO;
import dev.pulso.pulso.schedule.dto.ShiftSaveRequestDTO;
import dev.pulso.pulso.schedule.model.Allocation;
import dev.pulso.pulso.schedule.model.Schedule;
import dev.pulso.pulso.schedule.model.Shift;
import dev.pulso.pulso.schedule.model.enums.AllocationStatus;
import dev.pulso.pulso.schedule.model.enums.AllocationType;
import dev.pulso.pulso.schedule.repository.AllocationRepository;
import dev.pulso.pulso.schedule.repository.ScheduleRepository;
import dev.pulso.pulso.schedule.repository.ShiftRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
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
    public ScheduleShiftsDTO save(ShiftSaveRequestDTO request){
        Schedule schedule = scheduleRepo.findById(request.scheduleId())
                .orElseThrow(() -> new EntityNotFoundException("Schedule not found"));

        boolean isUpdate = request.id() != null;

        if (isUpdate){
            return update(request, schedule);
        }
        return create(request, schedule);

    }
    private ScheduleShiftsDTO create(ShiftSaveRequestDTO request, Schedule schedule) {

        Shift newShift = new Shift(
                request.date(),
                request.startTime(),
                request.endTime(),
                request.description(),
                schedule
        );
        List<Allocation> allocations = updateDoctorsToShift(newShift, request.doctorsAllocatedId());
        return new ScheduleShiftsDTO(
                newShift.getId(),
                newShift.getDate(),
                newShift.getStartTime(),
                newShift.getEndTime(),
                newShift.getDescription(),
                newShift.getType(), // supondo que Shift tenha um campo type
                allocations.stream()
                        .map(a -> new ScheduleShiftsDTO.AllocationDTO(
                                a.getId(),
                                a.getDoctor().getPhotoUrl(), // ou getPhoto(), depende do teu model
                                a.getDoctor().getProfessional().getUsername(),
                                a.getIsConflicted(),         // ou outra lógica se esse campo não for direto
                                a.getStatus() != null ? a.getStatus().name() : null
                        ))
                        .toList()
        );

    }

    private ScheduleShiftsDTO update(ShiftSaveRequestDTO request, Schedule schedule){}

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
