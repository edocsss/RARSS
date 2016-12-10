package com.fyp.service;

import android.app.Service;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Binder;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

import com.fyp.FYPApp;
import com.fyp.constant.FileNames;
import com.fyp.model.AccelerometerReading;
import com.fyp.task.SensorReadingHandler;
import com.fyp.util.FileUtil;

import java.util.ArrayList;

public class AccelerometerReaderService extends Service implements SensorEventListener {
    private final String TAG = "AccelerometerReaderServ";
    private SensorManager sensorManager;
    private Sensor accelerometerSensor;
    private ArrayList<AccelerometerReading> accelerometerReadings;
    private Handler handler;
    private final IBinder binder = new AccelerometerReaderBinder();
    private boolean storeReadings = true;

    public class AccelerometerReaderBinder extends Binder {
        public AccelerometerReaderService getService() {
            return AccelerometerReaderService.this;
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.setupService();
        this.startListeningAccelerometer();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        this.setupService();
        this.startListeningAccelerometer();
        this.storeReadings = false;
        return this.binder;
    }

    @Override
    public void onDestroy() {
        this.stopListeningAccelerometer();
    }

    private void setupService() {
        this.sensorManager = FYPApp.getSensorManager();
        this.accelerometerSensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        this.accelerometerReadings = new ArrayList<>();
        this.handler = new Handler();
    }

    private void startListeningAccelerometer() {
        this.sensorManager.registerListener(this, this.accelerometerSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningAccelerometer() {
        this.sensorManager.unregisterListener(this);
        if (this.storeReadings) this.storeAccelerometerReadingsToFile();
    }

    private void storeAccelerometerReadingsToFile() {
        FileUtil.writeFile(this, FileNames.ACCELEROMETER_RESULT, this.convertAccelerometerReadingToCSV().getBytes());
    }

    public synchronized String convertAccelerometerReadingToCSV() {
        ArrayList<AccelerometerReading> accelerometerReadings = (ArrayList<AccelerometerReading>) this.accelerometerReadings.clone();
        StringBuilder sb = new StringBuilder();
        sb.append("timestamp,ax,ay,az\n");

        for (AccelerometerReading ar: accelerometerReadings) {
            sb.append(ar.toString());
            sb.append("\n");
        }

        return sb.toString();
    }

    public void clearAccelerometerReadings() {
        this.accelerometerReadings.clear();
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