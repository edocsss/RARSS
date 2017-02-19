package com.fyp.activity;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.fyp.R;
import com.fyp.constant.SharedPreferencesKey;
import com.fyp.constant.TimerConfig;
import com.fyp.controller.RealTimeMonitoringController;
import com.fyp.controller.SharedPreferencesController;
import com.fyp.service.AccelerometerReaderService;
import com.fyp.service.BarometerReaderService;
import com.fyp.service.GyroscopeReaderService;
import com.fyp.task.RealTimeMonitoringDataHandler;
import com.fyp.util.AudioUtil;

public class RealTimeActivity extends AppCompatActivity {
    private final String TAG = "RealTimeActivity";
    private AccelerometerReaderService accelerometerReaderService;
    private GyroscopeReaderService gyroscopeReaderService;
    private BarometerReaderService barometerReaderService;
    private boolean accelerometerServiceBound = false;
    private boolean gyroscopeServiceBound = false;
    private boolean barometerServiceBound = false;
    private ServiceConnection accelerometerServiceConnection;
    private ServiceConnection gyroscopeServiceConnection;
    private ServiceConnection barometerServiceConnection;
    private Handler handler;

    private EditText intervalEditText;
    private Button startMonitoringButton;
    private final long NGROK_MAX_REQUEST_INTERVAL = (60 * 1000) / 20; // 20 connections per 60s
    private long timer;
    private long sleepTimer;
    private boolean stopTimer = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_real_time);
        this.getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        this.handler = new Handler();

        this.setupServiceConnection();
        this.setupReference();
        this.loadRealTimeIntervalPreferences();
    }

    @Override
    protected void onStop() {
        super.onStop();
        this.stopActivityMonitoring();
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                this.onBackPressed();
                return false;
        }

        return super.onOptionsItemSelected(item);
    }

    private void setupServiceConnection() {
        this.accelerometerServiceConnection = new ServiceConnection() {
            @Override
            public void onServiceConnected(ComponentName name, IBinder service) {
                AccelerometerReaderService.AccelerometerReaderBinder accelerometerBinder = (AccelerometerReaderService.AccelerometerReaderBinder) service;
                RealTimeActivity.this.accelerometerReaderService = accelerometerBinder.getService();
                RealTimeActivity.this.accelerometerServiceBound = true;
            }

            @Override
            public void onServiceDisconnected(ComponentName name) {
                RealTimeActivity.this.accelerometerServiceBound = false;
            }
        };

        this.gyroscopeServiceConnection = new ServiceConnection() {
            @Override
            public void onServiceConnected(ComponentName name, IBinder service) {
                GyroscopeReaderService.GyroscopeReaderBinder gyroscopeBinder = (GyroscopeReaderService.GyroscopeReaderBinder) service;
                RealTimeActivity.this.gyroscopeReaderService= gyroscopeBinder.getService();
                RealTimeActivity.this.gyroscopeServiceBound = true;
            }

            @Override
            public void onServiceDisconnected(ComponentName name) {
                RealTimeActivity.this.gyroscopeServiceBound = false;
            }
        };

        this.barometerServiceConnection = new ServiceConnection() {
            @Override
            public void onServiceConnected(ComponentName name, IBinder service) {
                BarometerReaderService.BarometerReaderBinder barometerBinder = (BarometerReaderService.BarometerReaderBinder) service;
                RealTimeActivity.this.barometerReaderService = barometerBinder.getService();
                RealTimeActivity.this.barometerServiceBound = true;
            }

            @Override
            public void onServiceDisconnected(ComponentName name) {
                RealTimeActivity.this.accelerometerServiceBound = false;
            }
        };
    }

    private void setupReference() {
        this.startMonitoringButton = (Button) this.findViewById(R.id.start_real_time_monitoring_button);
        this.intervalEditText = (EditText) this.findViewById(R.id.real_time_interval_edittext);
    }

    private void loadRealTimeIntervalPreferences() {
        this.timer = SharedPreferencesController.getInstance().getLong(SharedPreferencesKey.REAL_TIME_TIMER_KEY);
        if (this.timer == 0) this.timer = TimerConfig.DEFAULT_REAL_TIME_INTERVAL;

        this.setupSleepTimer();
        this.intervalEditText.setText("" + this.timer / 1000);
    }

    private void setupSleepTimer() {
        if (this.timer >= this.NGROK_MAX_REQUEST_INTERVAL) {
            this.sleepTimer = 0;
        } else {
            this.sleepTimer = (this.NGROK_MAX_REQUEST_INTERVAL - this.timer) + 100;
        }
    }

    private class ActivityMonitoringTimer extends AsyncTask<Void, Void, Void> {
        @Override
        protected Void doInBackground(Void... params) {
            long start = System.currentTimeMillis();
            long diff;

            while (!stopTimer) {
                diff = System.currentTimeMillis() - start;
                if (diff >= timer) {
                    String accelerometerReadingsString = accelerometerReaderService.convertAccelerometerReadingToCSV();
                    String gyroscopeReadingsString = gyroscopeReaderService.convertGyroscopeReadingToCSV();
                    String barometerReadingsString = barometerReaderService.convertBarometerReadingToCSV();

                    accelerometerReaderService.clearAccelerometerReadings();
                    gyroscopeReaderService.clearGyroscopeReadings();
                    barometerReaderService.clearBarometerReadings();

                    // Preventing NGROK TUNNEL 60s = max 20 connections violation
                    try {
                        Thread.sleep(sleepTimer);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                    handler.post(new RealTimeMonitoringDataHandler(accelerometerReadingsString, gyroscopeReadingsString, barometerReadingsString));
                    start = System.currentTimeMillis();
                } else {
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }

            return null;
        }
    }

    private void startActivityMonitoring() {
        Intent accelerometerServiceIntent = new Intent(this, AccelerometerReaderService.class);
        Intent gyroscopeServiceIntent = new Intent(this, GyroscopeReaderService.class);
        Intent barometerServiceIntent = new Intent(this, BarometerReaderService.class);

        this.bindService(accelerometerServiceIntent, this.accelerometerServiceConnection, Context.BIND_AUTO_CREATE);
        this.bindService(gyroscopeServiceIntent, this.gyroscopeServiceConnection, Context.BIND_AUTO_CREATE);
        this.bindService(barometerServiceIntent, this.barometerServiceConnection, Context.BIND_AUTO_CREATE);

        RealTimeMonitoringController.getInstance().startSmartwatchSensorMonitoring();
        this.stopTimer = false;
        new ActivityMonitoringTimer().execute();

        Toast.makeText(this, "Activity Monitoring Started!", Toast.LENGTH_SHORT).show();
        AudioUtil.playStartRecordingRingtone(this);
        this.startMonitoringButton.setEnabled(false);
    }

    private void stopActivityMonitoring() {
        if (this.accelerometerServiceBound && this.gyroscopeServiceBound && this.barometerServiceBound) {
            this.unbindService(this.accelerometerServiceConnection);
            this.unbindService(this.gyroscopeServiceConnection);
            this.unbindService(this.barometerServiceConnection);

            this.accelerometerServiceBound = false;
            this.gyroscopeServiceBound = false;
            this.barometerServiceBound = false;

            this.stopTimer = true;
            RealTimeMonitoringController.getInstance().stopSmartwatchSensorMonitoring();

            Toast.makeText(this, "Activity Monitoring Stopped!", Toast.LENGTH_SHORT).show();
            AudioUtil.playStopRecordingRingtone(this);
            this.startMonitoringButton.setEnabled(true);
        }
    }

    public void saveInterval(View v) {
        try {
            this.timer = Long.parseLong(this.intervalEditText.getText().toString()) * 1000;
            SharedPreferencesController.getInstance().setLong(SharedPreferencesKey.REAL_TIME_TIMER_KEY, this.timer);
        } catch (NumberFormatException e) {
            this.timer = TimerConfig.DEFAULT_REAL_TIME_INTERVAL;
        } finally {
            long timerInSecond = this.timer / 1000;
            this.setupSleepTimer();
            Toast.makeText(this, "Interval: " + timerInSecond + "s", Toast.LENGTH_SHORT).show();
        }
    }

    public void onStartMonitoringClick(View v) {
        this.startActivityMonitoring();
    }

    public void onStopMonitoringClick(View v) {
        this.stopActivityMonitoring();
    }
}
