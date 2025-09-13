package dev.pulso.pulso.account.model;

public enum Weekday {
    MONDAY("segunda"),
    TUESDAY("terça"),
    WEDNESDAY("quarta"),
    THURSDAY("quinta"),
    FRIDAY("sexta");

    private final String label;

    Weekday(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}