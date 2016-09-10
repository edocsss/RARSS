package com.fyp.handler;

import java.util.List;

public class SensorReadingHandler<T> implements Runnable {
    private T reading;
    private List<T> readings;

    public SensorReadingHandler(T reading, List<T> readings) {
        this.reading = reading;
        this.readings = readings;
    }

    @Override
    public void run() {
        this.readings.add(this.reading);
    }
}
