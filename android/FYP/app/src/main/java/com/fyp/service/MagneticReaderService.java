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
import com.fyp.model.MagneticReading;
import com.fyp.util.FileUtil;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class MagneticReaderService extends Service implements SensorEventListener {
    private final String TAG = "MagneticReaderServ";

    private SensorManager sensorManager;
    private Sensor magneticSensor;
    private List<MagneticReading> magneticReadings;
    private Handler handler;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.sensorManager = FYPApp.getSensorManager();
        this.magneticSensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
        this.magneticReadings = new ArrayList<>();
        this.handler = new Handler();

        this.startListeningMagnetic();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        this.stopListeningMagnetic();
    }

    private void startListeningMagnetic() {
        this.sensorManager.registerListener(this, this.magneticSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningMagnetic() {
        this.sensorManager.unregisterListener(this);
        this.storeMagneticReadingsToFile();
    }

    private void storeMagneticReadingsToFile() {
        FileUtil.writeFile(this, FileNames.MAGNETIC_RESULT, this.convertMagneticReadingToCSV().getBytes());
    }

    private String convertMagneticReadingToCSV() {
        StringBuilder sb = new StringBuilder();
        sb.append(new Date().toString());
        sb.append("\n");

        for (MagneticReading mr: this.magneticReadings) {
            sb.append(mr.toString());
            sb.append("\n");
        }

        return sb.toString();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        MagneticReading mr = new MagneticReading(
                System.currentTimeMillis(),
                event.values[0],
                event.values[1],
                event.values[2]
        );

        this.handler.post(new SensorReadingHandler<>(mr, magneticReadings));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        Log.i(TAG, "Accuracy changes: " + sensor.toString() + " " + accuracy);
    }
}