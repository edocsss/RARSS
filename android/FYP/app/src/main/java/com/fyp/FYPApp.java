package com.fyp;

import android.app.Application;
import android.content.Context;
import android.hardware.SensorManager;

import com.fyp.controller.FileIdController;
import com.fyp.controller.SensorController;
import com.fyp.controller.SharedPreferencesController;
import com.fyp.controller.UrlController;
import com.fyp.http.HttpManager;

public class FYPApp extends Application {
    public static final String APP_NAME = "FYPSensorDataCollector";
    private static SensorManager sensorManager;

    @Override
    public void onCreate () {
        super.onCreate();
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        HttpManager.init(this.getApplicationContext());
        SharedPreferencesController.init(this.getApplicationContext());

        SensorController.getInstance().detectAllAvailableSensors();
        FileIdController.getInstance().initFileId();
        UrlController.getInstance().initUrl();
    }

    public static SensorManager getSensorManager() {
        return sensorManager;
    }
}