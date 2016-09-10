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
import com.fyp.model.BarometerReading;
import com.fyp.util.FileUtil;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class BarometerReaderService extends Service implements SensorEventListener {
    private final String TAG = "BaroReaderServ";

    private SensorManager sensorManager;
    private Sensor barometerSensor;
    private List<BarometerReading> barometerReadings;
    private Handler handler;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.sensorManager = FYPApp.getSensorManager();
        this.barometerSensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_PRESSURE);
        this.barometerReadings = new ArrayList<>();
        this.handler = new Handler();

        this.startListeningBarometer();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        this.stopListeningBarometer();
    }

    private void startListeningBarometer() {
        this.sensorManager.registerListener(this, this.barometerSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningBarometer() {
        this.sensorManager.unregisterListener(this);
        this.storeBarometerReadingsToFile();
    }

    private void storeBarometerReadingsToFile() {
        FileUtil.writeFile(this, FileNames.BAROMETER_RESULT, this.convertBarometerReadingToCSV().getBytes());
    }

    private String convertBarometerReadingToCSV() {
        StringBuilder sb = new StringBuilder();
        sb.append(new Date().toString());
        sb.append("\n");

        for (BarometerReading br: this.barometerReadings) {
            sb.append(br.toString());
            sb.append("\n");
        }

        return sb.toString();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        BarometerReading br = new BarometerReading(
                System.currentTimeMillis(),
                event.values[0],
                event.values[1],
                event.values[2]
        );

        this.handler.post(new SensorReadingHandler<>(br, barometerReadings));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        Log.i(TAG, "Accuracy changes: " + sensor.toString() + " " + accuracy);
    }
}
