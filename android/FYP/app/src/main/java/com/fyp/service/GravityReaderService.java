package com.fyp.service;

import android.app.Service;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

import com.fyp.FYPApp;
import com.fyp.constant.FileNames;
import com.fyp.handler.SensorReadingHandler;
import com.fyp.model.GravityReading;
import com.fyp.util.FileUtil;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class GravityReaderService extends Service implements SensorEventListener {
    private final String TAG = "GravityReaderServ";

    private SensorManager sensorManager;
    private Sensor gravitySensor;
    private List<GravityReading> gravityReadings;
    private Handler handler;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.sensorManager = FYPApp.getSensorManager();
        this.gravitySensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY);
        this.gravityReadings = new ArrayList<>();
        this.handler = new Handler();

        this.startListeningGravity();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        this.stopListeningGravity();
    }

    private void startListeningGravity() {
        this.sensorManager.registerListener(this, this.gravitySensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningGravity() {
        this.sensorManager.unregisterListener(this);
        this.storeGravityReadingsToFile();
    }

    private void storeGravityReadingsToFile() {
        FileUtil.writeFile(this, FileNames.GRAVITY_RESULT, this.convertGravityReadingToCSV().getBytes());
    }

    private String convertGravityReadingToCSV() {
        StringBuilder sb = new StringBuilder();
        sb.append(new Date().toString());
        sb.append("\n");

        for (GravityReading gr: this.gravityReadings) {
            sb.append(gr.toString());
            sb.append("\n");
        }

        return sb.toString();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        GravityReading gr = new GravityReading(
                System.currentTimeMillis(),
                event.values[0],
                event.values[1],
                event.values[2]
        );

        this.handler.post(new SensorReadingHandler<>(gr, this.gravityReadings));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        Log.i(TAG, "Accuracy changes: " + sensor.toString() + " " + accuracy);
    }
}
