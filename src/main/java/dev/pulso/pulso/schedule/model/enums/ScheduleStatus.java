package dev.pulso.pulso.schedule.model.enums;

public enum ScheduleStatus {
    PUBLISHED("Publicado", "Published"),
    DRAFT("Rascunho", "Draft"),
    ARCHIVED("Arquivado", "Archived");

    private final String pt;
    private final String en;

    ScheduleStatus(String pt, String en) {
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
