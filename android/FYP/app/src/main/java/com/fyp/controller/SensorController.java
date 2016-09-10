package com.fyp.controller;

import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.util.Log;

import com.fyp.FYPApp;

import java.util.ArrayList;
import java.util.List;

public class SensorController {
    private static String TAG = "SensorController";
    private List<Sensor> availableSensors;
    private SensorManager sensorManager;
    private static SensorController instance = null;

    public SensorController(SensorManager sensorManager) {
        this.availableSensors = new ArrayList<>();
        this.sensorManager = sensorManager;
    }

    public static SensorController getInstance() {
        if (instance == null) {
            instance = new SensorController(FYPApp.getSensorManager());
        }

        return instance;
    }

    public List<Sensor> getAvailableSensors() {
        return availableSensors;
    }

    public void detectAllAvailableSensors() {
        Log.i(TAG, "Retrieving all available sensors on this device...");
        this.availableSensors = this.sensorManager.getSensorList(Sensor.TYPE_ALL);
        Log.i(TAG, "All available sensors are retrieved!");
    }
}
