package com.fyp.task;

import java.util.ArrayList;

public class SensorReadingHandler<T> implements Runnable {
    private T reading;
    private ArrayList<T> readings;

    public SensorReadingHandler(T reading, ArrayList<T> readings) {
        this.reading = reading;
        this.readings = readings;
    }

    @Override
    public void run() {
        this.readings.add(this.reading);
    }
}
