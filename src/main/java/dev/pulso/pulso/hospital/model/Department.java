package dev.pulso.pulso.hospital.model;

import dev.pulso.pulso.account.model.Manager;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

@Entity
@Table(name = "departments")
public class Department {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    @NotBlank(message = "O nome é obrigatório")
    @Pattern(regexp = "^[A-Za-z0-9\\s]+$", message = "O nome deve conter apenas letras, números e espaços.")
    private String name;

    @Column(nullable = false)
    private Boolean active = true;

    @ManyToOne
    @JoinColumn(name = "manager_id")
    private Manager manager;

    public Department() {}

    public Department(String name, Boolean active, Manager manager) {
        this.name = name;
        this.active = active;
        this.manager = manager;
    }

    // Getters e Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }

    public Manager getManager() { return manager; }
    public void setManager(Manager manager) { this.manager = manager; }

    @Override
    public String toString() {
        return this.name;
    }
}
