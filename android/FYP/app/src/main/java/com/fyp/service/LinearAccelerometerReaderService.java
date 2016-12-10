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

public class LinearAccelerometerReaderService extends Service implements SensorEventListener {
    private final String TAG = "LinAccReaderServ";

    private SensorManager sensorManager;
    private Sensor linearAccelerometerSensor;
    private ArrayList<AccelerometerReading> linearAccelerometerReadings;
    private Handler handler;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.sensorManager = FYPApp.getSensorManager();
        this.linearAccelerometerSensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
        this.linearAccelerometerReadings = new ArrayList<>();
        this.handler = new Handler();

        this.startListeningLinearAccelerometer();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        this.stopListeningLinearAccelerometer();
    }

    private void startListeningLinearAccelerometer() {
        this.sensorManager.registerListener(this, this.linearAccelerometerSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningLinearAccelerometer() {
        this.sensorManager.unregisterListener(this);
        this.storeLinearAccelerometerReadingsToFile();
    }

    private void storeLinearAccelerometerReadingsToFile() {
        FileUtil.writeFile(this, FileNames.LINEAR_ACCELEROMETER_RESULT, this.convertLinearAccelerometerReadingToCSV().getBytes());
    }

    private String convertLinearAccelerometerReadingToCSV() {
        StringBuilder sb = new StringBuilder();
        sb.append("timestamp,lax,lay,laz\n");

        for (AccelerometerReading ar: this.linearAccelerometerReadings) {
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

        this.handler.post(new SensorReadingHandler<>(ar, linearAccelerometerReadings));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        Log.i(TAG, "Accuracy changes: " + sensor.toString() + " " + accuracy);
    }
}