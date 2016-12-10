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
import com.fyp.task.RealTimeMonitoringDataHandler;
import com.fyp.util.AudioUtil;

public class RealTimeActivity extends AppCompatActivity {
    private final String TAG = "RealTimeActivity";
    private AccelerometerReaderService accelerometerReaderService;
    private boolean serviceBound = false;
    private ServiceConnection serviceConnection;
    private Handler handler;

    private EditText intervalEditText;
    private Button startMonitoringButton;
    private long timer;
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
        this.serviceConnection = new ServiceConnection() {
            @Override
            public void onServiceConnected(ComponentName name, IBinder service) {
                AccelerometerReaderService.AccelerometerReaderBinder binder = (AccelerometerReaderService.AccelerometerReaderBinder) service;
                RealTimeActivity.this.accelerometerReaderService = binder.getService();
                RealTimeActivity.this.serviceBound = true;
            }

            @Override
            public void onServiceDisconnected(ComponentName name) {
                RealTimeActivity.this.serviceBound = false;
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
        this.intervalEditText.setText("" + this.timer / 1000);
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
                    accelerometerReaderService.clearAccelerometerReadings();

                    handler.post(new RealTimeMonitoringDataHandler(accelerometerReadingsString));
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
        Intent serviceIntent = new Intent(this, AccelerometerReaderService.class);
        this.bindService(serviceIntent, this.serviceConnection, Context.BIND_AUTO_CREATE);

        RealTimeMonitoringController.getInstance().startSmartwatchSensorMonitoring();
        this.stopTimer = false;
        new ActivityMonitoringTimer().execute();

        Toast.makeText(this, "Activity Monitoring Started!", Toast.LENGTH_SHORT).show();
        AudioUtil.playStartRecordingRingtone(this);
        this.startMonitoringButton.setEnabled(false);
    }

    private void stopActivityMonitoring() {
        if (this.serviceBound) {
            this.unbindService(this.serviceConnection);
            this.serviceBound = false;
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
