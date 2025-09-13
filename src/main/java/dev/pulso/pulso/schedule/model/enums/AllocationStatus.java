package dev.pulso.pulso.schedule.model.enums;

public enum AllocationStatus {
    CONFIRMED("Confirmada", "Confirmed"),
    REJECTED("Recusada", "Rejected"),
    PENDING("Em Aberto", "Pending");

    private final String pt;
    private final String en;

    AllocationStatus(String pt, String en) {
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