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
import com.fyp.model.BarometerReading;
import com.fyp.task.SensorReadingHandler;
import com.fyp.util.FileUtil;

import java.util.ArrayList;

public class BarometerReaderService extends Service implements SensorEventListener {
    private final String TAG = "BaroReaderServ";
    private SensorManager sensorManager;
    private Sensor barometerSensor;
    private ArrayList<BarometerReading> barometerReadings;
    private Handler handler;
    private final IBinder binder = new BarometerReaderBinder();
    private boolean storeReadings = true;

    public class BarometerReaderBinder extends Binder {
        public BarometerReaderService getService() {
            return BarometerReaderService.this;
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.setupService();
        this.startListeningBarometer();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        this.setupService();
        this.startListeningBarometer();
        this.storeReadings = false;
        return this.binder;
    }

    @Override
    public void onDestroy() {
        this.stopListeningBarometer();
    }

    private void setupService() {
        this.sensorManager = FYPApp.getSensorManager();
        this.barometerSensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_PRESSURE);
        this.barometerReadings = new ArrayList<>();
        this.handler = new Handler();
    }

    private void startListeningBarometer() {
        this.sensorManager.registerListener(this, this.barometerSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningBarometer() {
        this.sensorManager.unregisterListener(this);
        if (this.storeReadings) this.storeBarometerReadingsToFile();
    }

    private void storeBarometerReadingsToFile() {
        FileUtil.writeFile(this, FileNames.BAROMETER_RESULT, this.convertBarometerReadingToCSV().getBytes());
    }

    public synchronized String convertBarometerReadingToCSV() {
        ArrayList<BarometerReading> barometerReadings = (ArrayList<BarometerReading>) this.barometerReadings.clone();
        StringBuilder sb = new StringBuilder();
        sb.append("timestamp,pressure\n");

        for (BarometerReading br: barometerReadings) {
            sb.append(br.toString());
            sb.append("\n");
        }

        return sb.toString();
    }

    public void clearBarometerReadings() {
        this.barometerReadings.clear();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        BarometerReading br = new BarometerReading(
                System.currentTimeMillis(),
                event.values[0]
        );

        this.handler.post(new SensorReadingHandler<>(br, barometerReadings));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        Log.i(TAG, "Barometer accuracy changes: " + sensor.toString() + " " + accuracy);
    }
}
