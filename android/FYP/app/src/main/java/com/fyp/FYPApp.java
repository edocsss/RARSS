package com.fyp;

import android.app.Application;
import android.content.Context;
import android.hardware.SensorManager;

import com.fyp.constant.SharedPreferencesKey;
import com.fyp.controller.SensorController;
import com.fyp.controller.SharedPreferencesController;

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
        this.initializeFileId();
    }

    public static Context getContext() {
        return context;
    }

    public static SensorManager getSensorManager() {
        return sensorManager;
    }

    public static int getNextFileIdAndIncrement() {
        int nextFileId = SharedPreferencesController.getInstance().getInt(SharedPreferencesKey.FILE_ID_KEY);
        SharedPreferencesController.getInstance().setInt(SharedPreferencesKey.FILE_ID_KEY, nextFileId + 1);
        return nextFileId;
    }

    private void initializeFileId() {
        if (SharedPreferencesController.getInstance().getInt(SharedPreferencesKey.FILE_ID_KEY) == 0) {
            SharedPreferencesController.getInstance().setInt(SharedPreferencesKey.FILE_ID_KEY, 70);
        }
    }
}