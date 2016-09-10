package com.fyp.activity;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.fyp.R;
import com.fyp.constant.FileNames;
import com.fyp.constant.SharedPreferencesKey;
import com.fyp.controller.SharedPreferencesController;
import com.fyp.http.HttpManager;
import com.fyp.service.AccelerometerReaderService;
import com.fyp.service.BarometerReaderService;
import com.fyp.service.GravityReaderService;
import com.fyp.service.GyroscopeReaderService;
import com.fyp.service.LinearAccelerometerReaderService;
import com.fyp.service.MagneticReaderService;
import com.fyp.util.FileUtil;

import org.json.JSONObject;

public class SensorReadingActivity extends AppCompatActivity {
    private final String TAG = "SensorReadingActivity";
    private final int DEFAULT_TIMER = 1000 * 60 * 2;

    private int timer;
    private Button startRecordingButton;
    private EditText timerEditText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sensor_reading);

        this.setupReference();
        this.loadTimerAndServerAddressPreferences();
    }

    private void setupReference() {
        this.startRecordingButton = (Button) this.findViewById(R.id.start_recording_button);
        this.timerEditText = (EditText) this.findViewById(R.id.timer_edittext);
    }

    private void loadTimerAndServerAddressPreferences() {
        this.timer = SharedPreferencesController.getInstance().getInt(SharedPreferencesKey.TIMER_KEY);
        if (this.timer == 0) this.timer = DEFAULT_TIMER;
        this.timerEditText.setText("" + this.timer);
    }

    public void startSensorRecording(View view) {
        // Need to spawn a timer thread to handle stopping

        Intent accelerometerReaderServiceIntent = new Intent(this, AccelerometerReaderService.class);
        Intent barometerReaderServiceIntent = new Intent(this, BarometerReaderService.class);
        Intent gravityReaderServiceIntent = new Intent(this, GravityReaderService.class);
        Intent gyroscopeReaderServiceIntent = new Intent(this, GyroscopeReaderService.class);
        Intent linearAccelerometerReaderServiceIntent = new Intent(this, LinearAccelerometerReaderService.class);
        Intent magneticReaderServiceIntent = new Intent(this, MagneticReaderService.class);

        this.startService(accelerometerReaderServiceIntent);
        this.startService(barometerReaderServiceIntent);
        this.startService(gravityReaderServiceIntent);
        this.startService(gyroscopeReaderServiceIntent);
        this.startService(linearAccelerometerReaderServiceIntent);
        this.startService(magneticReaderServiceIntent);

        this.startRecordingButton.setEnabled(false);
    }

    public void stopSensorRecording(View view) {
        Intent accelerometerReaderServiceIntent = new Intent(this, AccelerometerReaderService.class);
        Intent barometerReaderServiceIntent = new Intent(this, BarometerReaderService.class);
        Intent gravityReaderServiceIntent = new Intent(this, GravityReaderService.class);
        Intent gyroscopeReaderServiceIntent = new Intent(this, GyroscopeReaderService.class);
        Intent linearAccelerometerReaderServiceIntent = new Intent(this, LinearAccelerometerReaderService.class);
        Intent magneticReaderServiceIntent = new Intent(this, MagneticReaderService.class);

        this.stopService(accelerometerReaderServiceIntent);
        this.stopService(barometerReaderServiceIntent);
        this.stopService(gravityReaderServiceIntent);
        this.stopService(gyroscopeReaderServiceIntent);
        this.stopService(linearAccelerometerReaderServiceIntent);
        this.stopService(magneticReaderServiceIntent);

        this.startRecordingButton.setEnabled(true);

        // Should stop the timer thread as well (premature stopping)
    }

    public void saveTimer(View view) {
        try {
            this.timer = Integer.parseInt(this.timerEditText.getText().toString());
            SharedPreferencesController.getInstance().setInt(SharedPreferencesKey.TIMER_KEY, this.timer);
        } catch (NumberFormatException e) {
            this.timer = DEFAULT_TIMER;
        } finally {
            Toast.makeText(this, "Timer: " + this.timer, Toast.LENGTH_SHORT).show();
        }
    }

    public void sendFileToServer(View view) {
        final Response.Listener<JSONObject> onSuccess = new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Toast.makeText(SensorReadingActivity.this, "Sent to server!", Toast.LENGTH_SHORT).show();
            }
        };

        final Response.ErrorListener onError = new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(SensorReadingActivity.this, "Cannot send to server!", Toast.LENGTH_SHORT).show();
            }
        };

        new Thread(new Runnable() {
            @Override
            public void run() {
                String accelerometerResultFileContent = FileUtil.readFile(SensorReadingActivity.this, FileNames.ACCELEROMETER_RESULT);
                String barometerResultFileContent = FileUtil.readFile(SensorReadingActivity.this, FileNames.BAROMETER_RESULT);
                String gravityResultFileContent = FileUtil.readFile(SensorReadingActivity.this, FileNames.GRAVITY_RESULT);
                String gyroscopeResultFileContent = FileUtil.readFile(SensorReadingActivity.this, FileNames.GYROSCOPE_RESULT);
                String linearAccelerometerResultFileContent = FileUtil.readFile(SensorReadingActivity.this, FileNames.LINEAR_ACCELEROMETER_RESULT);
                String magneticResultFileContent = FileUtil.readFile(SensorReadingActivity.this, FileNames.MAGNETIC_RESULT);

                HttpManager.getInstance().sendFileContent(FileNames.ACCELEROMETER_RESULT, accelerometerResultFileContent, onSuccess, onError);
                HttpManager.getInstance().sendFileContent(FileNames.BAROMETER_RESULT, barometerResultFileContent, onSuccess, onError);
                HttpManager.getInstance().sendFileContent(FileNames.GRAVITY_RESULT, gravityResultFileContent, onSuccess, onError);
                HttpManager.getInstance().sendFileContent(FileNames.GYROSCOPE_RESULT, gyroscopeResultFileContent, onSuccess, onError);
                HttpManager.getInstance().sendFileContent(FileNames.LINEAR_ACCELEROMETER_RESULT, linearAccelerometerResultFileContent, onSuccess, onError);
                HttpManager.getInstance().sendFileContent(FileNames.MAGNETIC_RESULT, magneticResultFileContent, onSuccess, onError);
            }
        }).start();
    }
}
