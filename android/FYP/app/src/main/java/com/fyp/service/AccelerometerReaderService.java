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
import com.fyp.task.SensorReadingHandler;
import com.fyp.model.AccelerometerReading;
import com.fyp.util.FileUtil;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class AccelerometerReaderService extends Service implements SensorEventListener {
    private final String TAG = "AccelerometerReaderServ";

    private SensorManager sensorManager;
    private Sensor accelerometerSensor;
    private List<AccelerometerReading> accelerometerReadings;
    private Handler handler;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.sensorManager = FYPApp.getSensorManager();
        this.accelerometerSensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        this.accelerometerReadings = new ArrayList<>();
        this.handler = new Handler();

        this.startListeningAccelerometer();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        this.stopListeningAccelerometer();
    }

    private void startListeningAccelerometer() {
        this.sensorManager.registerListener(this, this.accelerometerSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningAccelerometer() {
        this.sensorManager.unregisterListener(this);
        this.storeAccelerometerReadingsToFile();
    }

    private void storeAccelerometerReadingsToFile() {
        FileUtil.writeFile(this, FileNames.ACCELEROMETER_RESULT, this.convertAccelerometerReadingToCSV().getBytes());
    }

    private String convertAccelerometerReadingToCSV() {
        StringBuilder sb = new StringBuilder();
        sb.append(new Date().toString());
        sb.append("\n");

        for (AccelerometerReading ar: this.accelerometerReadings) {
            sb.append(ar.toString());
            sb.append("\n");
        }

        return sb.toString();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        AccelerometerReading ar = new AccelerometerReading(
                System.currentTimeMillis(),
                event.values[0],
                event.values[1],
                event.values[2]
        );

        this.handler.post(new SensorReadingHandler<>(ar, accelerometerReadings));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        Log.i(TAG, "Accuracy changes: " + sensor.toString() + " " + accuracy);
    }
}