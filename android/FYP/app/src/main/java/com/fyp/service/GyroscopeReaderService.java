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
import com.fyp.model.GyroscopeReading;
import com.fyp.util.FileUtil;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class GyroscopeReaderService extends Service implements SensorEventListener {
    private final String TAG = "GyroReaderServ";

    private SensorManager sensorManager;
    private Sensor gyroscopeSensor;
    private List<GyroscopeReading> gyroscopeReadings;
    private Handler handler;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.sensorManager = FYPApp.getSensorManager();
        this.gyroscopeSensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        this.gyroscopeReadings = new ArrayList<>();
        this.handler = new Handler();

        this.startListeningGyroscope();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        this.stopListeningGyroscope();
    }

    private void startListeningGyroscope() {
        this.sensorManager.registerListener(this, this.gyroscopeSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningGyroscope() {
        this.sensorManager.unregisterListener(this);
        this.storeGyroscopeReadingsToFile();
    }

    private void storeGyroscopeReadingsToFile() {
        FileUtil.writeFile(this, FileNames.GYROSCOPE_RESULT, this.convertGyroscopeReadingToCSV().getBytes());
    }

    private String convertGyroscopeReadingToCSV() {
        StringBuilder sb = new StringBuilder();
        sb.append(new Date().toString());
        sb.append("\n");

        for (GyroscopeReading gr: this.gyroscopeReadings) {
            sb.append(gr.toString());
            sb.append("\n");
        }

        return sb.toString();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        GyroscopeReading gr = new GyroscopeReading(
                System.currentTimeMillis(),
                event.values[0],
                event.values[1],
                event.values[2]
        );

        this.handler.post(new SensorReadingHandler<>(gr, gyroscopeReadings));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        Log.i(TAG, "Accuracy changes: " + sensor.toString() + " " + accuracy);
    }
}
