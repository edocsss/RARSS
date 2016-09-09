package com.fyp.model;

public abstract class SensorReading {
    private long timestamp;

    public SensorReading(long timestamp) {
        this.timestamp = timestamp;
    }

    public long getTimestamp() {
        return timestamp;
    }
}
