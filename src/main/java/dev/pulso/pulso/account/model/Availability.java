package dev.pulso.pulso.account.model;

import jakarta.persistence.*;

@Entity
@Table(
        name = "availabilities",
        uniqueConstraints = @UniqueConstraint(columnNames = {"doctor_id", "day", "shift"})
)
public class Availability {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Weekday day;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ShiftPeriod shift;

    @ManyToOne
    @JoinColumn(name = "doctor_id", nullable = false)
    private Doctor doctor;

    // Construtores
    public Availability() {}

    public Availability(Doctor doctor, Weekday day, ShiftPeriod shift) {
        this.doctor = doctor;
        this.day = day;
        this.shift = shift;
    }

    // Getters e setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Weekday getDay() { return day; }
    public void setDay(Weekday day) { this.day = day; }

    public ShiftPeriod getShift() { return shift; }
    public void setShift(ShiftPeriod shift) { this.shift = shift; }

    public Doctor getDoctor() { return doctor; }
    public void setDoctor(Doctor doctor) { this.doctor = doctor; }

    @Override
    public String toString() {
        return doctor.getProfessional().getUsername() + " - " + day.getLabel() + " (" + shift.getLabel() + ")";
    }
}
