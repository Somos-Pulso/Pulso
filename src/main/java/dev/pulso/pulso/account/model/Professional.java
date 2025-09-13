package dev.pulso.pulso.account.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Entity
@Table(name = "professionals")
public class Professional {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    @NotBlank
    private String username;

    @Column(nullable = false)
    @Email
    @NotBlank
    private String email;

    @Column(unique = true)
    @Pattern(regexp = "\\d{11}", message = "CPF deve conter exatamente 11 dígitos numéricos")
    private String cpf;

    @Column(nullable = false)
    @Pattern(regexp = "\\d{10,11}", message = "Telefone deve conter 10 ou 11 dígitos")
    private String phone;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String profilePicture; // Pode armazenar path ou URL

    @Column(nullable = false)
    private String password;

    @OneToOne(mappedBy = "professional", cascade = CascadeType.ALL)
    private Manager manager;

    @OneToOne(mappedBy = "professional", cascade = CascadeType.ALL)
    private Doctor doctor;

    public Professional() {}

    public Professional(String username, String email, String cpf, String phone, String description, String password) {
        this.username = username;
        this.email = email;
        this.cpf = cpf;
        this.phone = phone;
        this.description = description;
        setPassword(password);
    }

    // Getters e setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getCpf() { return cpf; }
    public void setCpf(String cpf) {
        if (!cpfValid(cpf)) {
            throw new IllegalArgumentException("CPF inválido");
        }
        this.cpf = cpf;
    }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getProfilePicture() { return profilePicture; }
    public void setProfilePicture(String profilePicture) { this.profilePicture = profilePicture; }

    public String getPassword() { return password; }

    public void setPassword(String password) {
        if (password != null && !password.startsWith("$2a$")) { // BCrypt prefix
            BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
            this.password = encoder.encode(password);
        } else {
            this.password = password;
        }
    }

    // Propriedades derivadas
    @Transient
    public boolean isDoctor() {
        return doctor != null;
    }

    @Transient
    public boolean isManager() {
        return manager != null;
    }

    // Validação de CPF
    private boolean cpfValid(String cpf) {
        if (cpf == null || !cpf.matches("\\d{11}")) return false;
        if (cpf.chars().distinct().count() == 1) return false;

        int soma1 = 0;
        for (int i = 0; i < 9; i++) soma1 += Character.getNumericValue(cpf.charAt(i)) * (10 - i);
        int d1 = (soma1 * 10) % 11;
        if (d1 == 10) d1 = 0;

        int soma2 = 0;
        for (int i = 0; i < 10; i++) soma2 += Character.getNumericValue(cpf.charAt(i)) * (11 - i);
        int d2 = (soma2 * 10) % 11;
        if (d2 == 10) d2 = 0;

        return cpf.endsWith("" + d1 + d2);
    }

    @Override
    public String toString() {
        return this.username;
    }
}
