package com.fyp.model;

public class BarometerReading extends SensorReading {
    private double pressure;

    public BarometerReading(long timestamp, double pressure) {
        super(timestamp);
        this.pressure = pressure;
    }

    public double getPressure() {
        return pressure;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.getTimestamp());
        sb.append(",");
        sb.append(this.getPressure());

        return sb.toString();
    }
}
