package dev.pulso.pulso.schedule.model;

import dev.pulso.pulso.hospital.model.Department;
import dev.pulso.pulso.schedule.model.enums.ScheduleStatus;
import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.regex.Pattern;

@Entity
@Table(
        name = "schedules",
        uniqueConstraints = @UniqueConstraint(
                columnNames = {"name", "start_date", "end_date", "department_id"}
        )
)
public class Schedule {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 100, nullable = false)
    private String name;

    @Column(name = "start_date", nullable = false)
    private LocalDate startDate;

    @Column(name = "end_date", nullable = false)
    private LocalDate endDate;

    @Enumerated(EnumType.STRING)
    @Column(length = 20, nullable = false)
    private ScheduleStatus status;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id", nullable = false)
    private Department department;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    protected Schedule() {}

    public static Schedule create(String name, LocalDate startDate, LocalDate endDate,
                                  ScheduleStatus status, Department department) {

        if (name == null || name.isBlank())
            throw new IllegalArgumentException("Name cannot be blank");
        long letters = Pattern.compile("[A-Za-zÀ-ÿ]")
                .matcher(name)
                .results()
                .count();
        if (letters < 3)
            throw new IllegalArgumentException("Name must contain at least 3 letters");

        if (startDate == null || endDate == null)
            throw new IllegalArgumentException("Start and end dates cannot be null");
        if (startDate.isAfter(endDate))
            throw new IllegalArgumentException("Start date must be before end date");

        LocalDate today = LocalDate.now();
        LocalDate maxDate = LocalDate.of(2100, 12, 31);
        if (startDate.isBefore(today) || startDate.isAfter(maxDate) ||
                endDate.isBefore(today) || endDate.isAfter(maxDate))
            throw new IllegalArgumentException("Dates must be between today and 31/12/2100");

        if (department == null)
            throw new IllegalArgumentException("Department cannot be null");
        if (status == null)
            status = ScheduleStatus.DRAFT;

        Schedule schedule = new Schedule();
        schedule.name = name.trim();
        schedule.startDate = startDate;
        schedule.endDate = endDate;
        schedule.status = status;
        schedule.department = department;
        schedule.createdAt = LocalDateTime.now();
        schedule.updatedAt = LocalDateTime.now();

        return schedule;
    }

    // Atualiza updatedAt automaticamente
    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

    // Getters e Setters
    public Long getId() { return id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public LocalDate getStartDate() { return startDate; }
    public void setStartDate(LocalDate startDate) { this.startDate = startDate; }

    public LocalDate getEndDate() { return endDate; }
    public void setEndDate(LocalDate endDate) { this.endDate = endDate; }

    public ScheduleStatus getStatus() { return status; }
    public void setStatus(ScheduleStatus status) { this.status = status; }

    public Department getDepartment() { return department; }
    public void setDepartment(Department department) { this.department = department; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}
