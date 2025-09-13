package dev.pulso.pulso.schedule.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Entity
@Table(name = "shift")
public class Shift {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull
    private LocalDate date;

    @NotNull
    private LocalTime startTime;

    @NotNull
    private LocalTime endTime;

    @Lob
    private String description;

    @ManyToOne
    @JoinColumn(name = "schedule_id", nullable = false)
    private Schedule schedule;

    @Column(name = "created_at", updatable = false)
    private LocalDate createdAt;

    @Column(name = "updated_at")
    private LocalDate updatedAt;

    @OneToMany(mappedBy = "shift", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Allocation> allocations;

    protected Shift(){};

    public Shift(LocalDate date, LocalTime startTime, LocalTime endTime, String description, Schedule schedule){
        this.date = date;
        this.startTime = startTime;
        this.endTime = endTime;
        this.description = description;
        this.schedule = schedule;
    }


    // ===== GETTERS E SETTERS =====

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public LocalTime getStartTime() {
        return startTime;
    }

    public void setStartTime(LocalTime startTime) {
        this.startTime = startTime;
    }

    public LocalTime getEndTime() {
        return endTime;
    }

    public void setEndTime(LocalTime endTime) {
        this.endTime = endTime;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Schedule getSchedule() {
        return schedule;
    }

    public void setSchedule(Schedule schedule) {
        this.schedule = schedule;
    }

    public LocalDate getCreatedAt() {
        return createdAt;
    }

    public LocalDate getUpdatedAt() {
        return updatedAt;
    }

    public List<Allocation> getAllocations() {
        return allocations;
    }

    public void setAllocations(List<Allocation> allocations) {
        this.allocations = allocations;
    }

    // ===== MÉTODOS EQUIVALENTES AO @property DO DJANGO =====

    @Transient
    public String getType() {
        return (allocations != null && !allocations.isEmpty()) ? "ok-event" : "warn-event";
    }

    @Transient
    public Duration getDuration() {
        return Duration.between(startTime, endTime);
    }

    // ===== VALIDAÇÃO E CONTROLE DE DATAS =====

    @PrePersist
    public void prePersist() {
        this.createdAt = LocalDate.now();
        this.updatedAt = LocalDate.now();
        validate();
    }

    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDate.now();
        validate();
    }

    private void validate() {
        Map<String, String> errors = new HashMap<>();

        if (startTime != null && endTime != null && startTime.equals(endTime)) {
            errors.put("startTime", "Horário de início e fim não podem ser iguais.");
        }

        if (!errors.isEmpty()) {
            throw new IllegalArgumentException(errors.toString());
        }
    }

    @Override
    public String toString() {
        return String.format(
                "Shift on %s from %s to %s",
                date != null ? date.toString() : "null",
                startTime != null ? startTime.toString() : "null",
                endTime != null ? endTime.toString() : "null"
        );
    }
}
