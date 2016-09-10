package com.fyp.model;

public class GyroscopeReading extends SensorReading {
    private float gx, gy, gz;

    public GyroscopeReading(long timestamp, float gx, float gy, float gz) {
        super(timestamp);
        this.gx = gx;
        this.gy = gy;
        this.gz = gz;
    }

    public float getGx() {
        return gx;
    }

    public float getGy() {
        return gy;
    }

    public float getGz() {
        return gz;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.getTimestamp());
        sb.append(",");
        sb.append(this.getGx());
        sb.append(",");
        sb.append(this.getGy());
        sb.append(",");
        sb.append(this.getGz());

        return sb.toString();
    }
}
