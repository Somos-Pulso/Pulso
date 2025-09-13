package dev.pulso.pulso.schedule.model.enums;

public enum AllocationType {
    SUGGESTED("Sugestão", "Suggested"),
    DIRECT("Direta", "Direct");

    private final String pt;
    private final String en;

    AllocationType(String pt, String en) {
        this.pt = pt;
        this.en = en;
    }

    public String getPt() {
        return pt;
    }

    public String getEn() {
        return en;
    }
}

