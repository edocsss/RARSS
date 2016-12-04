package com.fyp.activity;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.IBinder;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

import com.fyp.R;
import com.fyp.service.AccelerometerReaderService;

public class RealTimeActivity extends AppCompatActivity {
    private AccelerometerReaderService accelerometerReaderService;
    private boolean serviceBound = false;
    private ServiceConnection serviceConnection;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_real_time);

        this.setupServiceConnection();
    }

    @Override
    protected void onStop() {
        super.onStop();

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

    private void startActivityMonitoring() {
        Intent serviceIntent = new Intent(this, AccelerometerReaderService.class);
        this.bindService(serviceIntent, this.serviceConnection, Context.BIND_AUTO_CREATE);

        // Need to make a timer Async class to keep track when to send the data to server!!
        // That timer class can access the ArrayList data

        Toast.makeText(this, "Activity Monitoring Started!", Toast.LENGTH_SHORT).show();
        // Disable button
    }

    private void stopActivityMonitoring() {
        if (this.serviceBound) {
            this.unbindService(this.serviceConnection);
            this.serviceBound = false;
            Toast.makeText(this, "Activity Monitoring Stopped!", Toast.LENGTH_SHORT).show();
        }
    }
}
