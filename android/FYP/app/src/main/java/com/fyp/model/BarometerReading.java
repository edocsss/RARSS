package com.fyp.model;

public class BarometerReading extends SensorReading {
    private float bx, by, bz;

    public BarometerReading(long timestamp, float bx, float by, float bz) {
        super(timestamp);
        this.bx = bx;
        this.by = by;
        this.bz = bz;
    }

    public float getBx() {
        return bx;
    }

    public float getBy() {
        return by;
    }

    public float getBz() {
        return bz;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.getTimestamp());
        sb.append(",");
        sb.append(this.getBx());
        sb.append(",");
        sb.append(this.getBy());
        sb.append(",");
        sb.append(this.getBz());

        return sb.toString();
    }
}
