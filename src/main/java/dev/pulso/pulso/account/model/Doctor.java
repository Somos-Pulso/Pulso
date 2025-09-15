package dev.pulso.pulso.account.model;

import dev.pulso.pulso.hospital.model.Department;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.time.Duration;
import java.util.Set;

@Entity
@Table(name = "doctors")
public class Doctor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Lado proprietário da relação com Professional
    @OneToOne
    @JoinColumn(name = "professional_id", nullable = false)
    private Professional professional;

    @Column(unique = true, nullable = false)
    @Pattern(
            regexp = "^\\d{4,6}(/(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO))?$",
            message = "Formato de CRM inválido. Use até 6 dígitos, opcionalmente seguidos de /UF (ex: 123456/SP)."
    )
    private String crm;

    @Column(nullable = false)
    private Duration workload;

    @ManyToMany
    @JoinTable(
            name = "doctor_departments",
            joinColumns = @JoinColumn(name = "doctor_id"),
            inverseJoinColumns = @JoinColumn(name = "department_id")
    )
    private Set<Department> departments;

    @ManyToMany
    @JoinTable(
            name = "doctor_specialties",
            joinColumns = @JoinColumn(name = "doctor_id"),
            inverseJoinColumns = @JoinColumn(name = "specialty_id")
    )
    private Set<Specialty> specialties;

    // Construtores
    public Doctor() {}

    public Doctor(Professional professional, String crm, Duration workload) {
        this.professional = professional;
        this.crm = crm;
        this.workload = workload;
    }

    // Getters e setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Professional getProfessional() { return professional; }
    public void setProfessional(Professional professional) { this.professional = professional; }

    public String getCrm() { return crm; }
    public void setCrm(String crm) { this.crm = crm; }

    public Duration getWorkload() { return workload; }
    public void setWorkload(Duration workload) {
        if (workload.toHours() > 744) {
            throw new IllegalArgumentException("Carga horária não pode ultrapassar 744 horas mensais.");
        }
        this.workload = workload;
    }

    public Set<Department> getDepartments() { return departments; }
    public void setDepartments(Set<Department> departments) { this.departments = departments; }

    public Set<Specialty> getSpecialties() { return specialties; }
    public void setSpecialties(Set<Specialty> specialties) { this.specialties = specialties; }

    // Propriedades derivadas
    @Transient
    public Duration getWorkHours() {
        // Aqui você precisa implementar a lógica de alocações do seu sistema
        // Por enquanto retorna zero
        return Duration.ZERO;
    }

    @Transient
    public boolean isFullyBooked() {
        return getWorkHours().compareTo(workload) >= 0;
    }

    @Override
    public String toString() {
        return "ID: " + professional.getId() + " - Dr. " + professional.getUsername() + " - CRM: " + crm;
    }
}