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
    private ArrayList<GyroscopeReading> gyroscopeReadings;
    private Handler handler;
    private final IBinder binder = new GyroscopeReaderBinder();
    private boolean storeReadings = true;

    public class GyroscopeReaderBinder extends Binder {
        public GyroscopeReaderService getService() {
            return GyroscopeReaderService.this;
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.setupService();
        this.startListeningGyroscope();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        this.setupService();
        this.startListeningGyroscope();
        this.storeReadings = false;
        return this.binder;
    }

    @Override
    public void onDestroy() {
        this.stopListeningGyroscope();
    }

    private void setupService() {
        this.sensorManager = FYPApp.getSensorManager();
        this.gyroscopeSensor = this.sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        this.gyroscopeReadings = new ArrayList<>();
        this.handler = new Handler();
    }

    private void startListeningGyroscope() {
        this.sensorManager.registerListener(this, this.gyroscopeSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopListeningGyroscope() {
        this.sensorManager.unregisterListener(this);
        if (this.storeReadings) this.storeGyroscopeReadingsToFile();
    }

    private void storeGyroscopeReadingsToFile() {
        FileUtil.writeFile(this, FileNames.GYROSCOPE_RESULT, this.convertGyroscopeReadingToCSV().getBytes());
    }

    public synchronized String convertGyroscopeReadingToCSV() {
        ArrayList<GyroscopeReading> gyroscopeReadings = (ArrayList<GyroscopeReading>) this.gyroscopeReadings.clone();
        StringBuilder sb = new StringBuilder();
        sb.append("timestamp,gx,gy,gz\n");

        for (GyroscopeReading gr: gyroscopeReadings) {
            sb.append(gr.toString());
            sb.append("\n");
        }

        return sb.toString();
    }

    public void clearGyroscopeReadings() {
        this.gyroscopeReadings.clear();
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
