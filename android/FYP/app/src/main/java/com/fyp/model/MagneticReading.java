package com.fyp.model;

public class MagneticReading extends SensorReading {
    private double mx, my, mz;

    public MagneticReading(long timestamp, double mx, double my, double mz) {
        super(timestamp);
        this.mx = mx;
        this.my = my;
        this.mz = mz;
    }

    public double getMx() {
        return mx;
    }

    public double getMy() {
        return my;
    }

    public double getMz() {
        return mz;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.getTimestamp());
        sb.append(",");
        sb.append(this.getMx());
        sb.append(",");
        sb.append(this.getMy());
        sb.append(",");
        sb.append(this.getMz());

        return sb.toString();
    }
}
