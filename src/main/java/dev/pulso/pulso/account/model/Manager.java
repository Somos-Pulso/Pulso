package dev.pulso.pulso.account.model;

import jakarta.persistence.*;

@Entity
@Table(name = "managers")
public class Manager {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Lado proprietário da relação (FK para Professional)
    @OneToOne
    @JoinColumn(name = "professional_id", nullable = false)
    private Professional professional;

    // Construtor padrão
    public Manager() {}

    // Construtor com Professional
    public Manager(Professional professional) {
        this.professional = professional;
    }

    // Getters e setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Professional getProfessional() {
        return professional;
    }

    public void setProfessional(Professional professional) {
        this.professional = professional;
    }

    @Override
    public String toString() {
        return "Manager: " + professional.getUsername();
    }
}
