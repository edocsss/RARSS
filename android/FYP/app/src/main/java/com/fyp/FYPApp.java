package com.fyp;

import android.app.Application;
import android.content.Context;
import android.hardware.SensorManager;

import com.fyp.controller.SensorController;

public class FYPApp extends Application {
    public static final String APP_NAME = "FYPSensorDataCollector";
    private static Context context;
    private static SensorManager sensorManager;

    @Override
    public void onCreate () {
        super.onCreate();
        context = getApplicationContext();
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        SensorController.getInstance().detectAllAvailableSensors();
    }

    public static Context getContext() {
        return context;
    }

    public static SensorManager getSensorManager() {
        return sensorManager;
    }
}
