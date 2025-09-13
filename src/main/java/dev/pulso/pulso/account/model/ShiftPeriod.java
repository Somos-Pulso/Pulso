package dev.pulso.pulso.account.model;

public enum ShiftPeriod {
    DAY("dia"),
    AFTERNOON("tarde"),
    NIGHT("noite");

    private final String label;

    ShiftPeriod(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}