package dev.pulso.pulso.schedule.model;

import dev.pulso.pulso.account.model.Doctor;
import dev.pulso.pulso.schedule.model.enums.AllocationStatus;
import dev.pulso.pulso.schedule.model.enums.AllocationType;
import jakarta.persistence.*;
import java.time.LocalDate;


@Entity
@Table(name = "allocations")
public class Allocation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @Column(length = 20, nullable = false)
    private AllocationType type;

    @Column(name = "return_date")
    private LocalDate returnDate ;

    @Enumerated(EnumType.STRING)
    @Column(length = 20, nullable = false)
    private AllocationStatus status;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "shift_id", nullable = false)
    private Shift shift;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "doctor_id", nullable = false)
    private Doctor doctor;

    @Column(name = "created_at", updatable = false)
    private LocalDate createdAt;

    @Column(name = "updated_at")
    private LocalDate updatedAt;

    protected Allocation() {}
    public Allocation( Shift shift, Doctor doctor, LocalDate returnDate, AllocationType type, AllocationStatus status) {
        this.shift = shift;
        this.doctor = doctor;
        this.type = (type != null) ? type : AllocationType.DIRECT;
        this.status = (status != null) ? status : AllocationStatus.CONFIRMED;
        this.returnDate = (returnDate != null) ? returnDate : LocalDate.now();
    }

    @PrePersist
    private void prePersist() {
        this.createdAt = LocalDate.now();
        this.updatedAt = LocalDate.now();
    }

    @PreUpdate
    private void preUpdate() {
        this.updatedAt = LocalDate.now();
    }

    @Override
    public String toString() {
        String docName = (doctor != null && doctor.getProfessional() != null)
                ? doctor.getProfessional().getUsername()
                : "null";
        String shiftDate = (shift != null) ? String.valueOf(shift.getDate()) : "null";
        return docName + " - " + shiftDate + " - " + type;
    }

    // Getters e Setters
    public Long getId() {return id;}
    public void setId(Long id) {this.id = id;}

    public AllocationType getType() {return type;}
    public void setType(AllocationType type) {this.type = type;}

    public LocalDate getReturnDate() {return returnDate;}
    public void setReturnDate(LocalDate returnDate) {this.returnDate = returnDate;}

    public AllocationStatus getStatus() {return status;}
    public void setStatus(AllocationStatus status) {this.status = status;}

    public Shift getShift() {return shift;}
    public void setShift(Shift shift) {this.shift = shift;}

    public Doctor getDoctor() {return doctor;}
    public void setDoctor(Doctor doctor) {this.doctor = doctor;}

    public LocalDate getCreatedAt() {return createdAt;}
    public LocalDate getUpdatedAt() {return updatedAt;}
}
