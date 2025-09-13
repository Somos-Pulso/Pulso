package dev.pulso.pulso.schedule.service.schedule;

import dev.pulso.pulso.hospital.model.Department;
import dev.pulso.pulso.schedule.model.Schedule;
import dev.pulso.pulso.schedule.model.enums.ScheduleStatus;
import dev.pulso.pulso.schedule.repository.ScheduleRepository;
import dev.pulso.pulso.hospital.repository.DepartmentRepository;
import dev.pulso.pulso.account.repository.ManagerRepository;
import dev.pulso.pulso.exception.ScheduleAlreadyExistsException;
import dev.pulso.pulso.exception.DepartmentNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import dev.pulso.pulso.account.model.Manager;

import java.time.LocalDate;
import java.util.List;

@Service
public class CreateScheduleService {

    private final ScheduleRepository scheduleRepository;
    private final DepartmentRepository departmentRepository;
    private final ManagerRepository managerRepository;

    public CreateScheduleService(ScheduleRepository scheduleRepository,
                                 DepartmentRepository departmentRepository,
                                 ManagerRepository managerRepository) {
        this.scheduleRepository = scheduleRepository;
        this.departmentRepository = departmentRepository;
        this.managerRepository = managerRepository;
    }

    @Transactional(readOnly = true)
    public List<Department> getDepartmentsByUserId(Long userId) {
        Manager manager = managerRepository.findByProfessionalId(userId);
        return manager != null
                ? departmentRepository.findByManagerAndActiveTrue(manager)
                : List.of();
    }

    @Transactional
    public Schedule createSchedule(String name, LocalDate startDate, LocalDate endDate, Long departmentId) {
        String formattedName = name.trim();

        Department department = departmentRepository.findById(departmentId)
                .orElseThrow(() -> new DepartmentNotFoundException("Departamento não encontrado"));

        boolean exists = scheduleRepository.existsByNameAndStartDateAndEndDateAndDepartmentId(
                formattedName, startDate, endDate, department.getId()
        );

        if (exists) {
            throw new ScheduleAlreadyExistsException("Já existe uma escala com essas informações nesse setor.");
        }

        Schedule newSchedule = Schedule.create(
                formattedName,
                startDate,
                endDate,
                ScheduleStatus.DRAFT,
                department
        );

        return scheduleRepository.save(newSchedule);
    }
}
