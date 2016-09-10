package com.fyp.model;

public class GravityReading extends SensorReading {
    private double gx, gy, gz;

    public GravityReading(long timestamp, double gx, double gy, double gz) {
        super(timestamp);
        this.gx = gx;
        this.gy = gy;
        this.gz = gz;
    }

    public double getGx() {
        return gx;
    }

    public double getGy() {
        return gy;
    }

    public double getGz() {
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
