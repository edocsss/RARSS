package com.fyp.activity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.fyp.R;
import com.fyp.constant.SharedPreferencesKey;
import com.fyp.constant.URL;
import com.fyp.controller.FileIdController;
import com.fyp.controller.SensorController;
import com.fyp.controller.SharedPreferencesController;
import com.fyp.controller.UrlController;
import com.fyp.service.AccelerometerReaderService;
import com.fyp.service.BarometerReaderService;
import com.fyp.service.GravityReaderService;
import com.fyp.service.GyroscopeReaderService;
import com.fyp.service.LinearAccelerometerReaderService;
import com.fyp.service.MagneticReaderService;
import com.fyp.util.AudioUtil;

import org.json.JSONObject;

public class RecorderActivity extends AppCompatActivity implements OnItemSelectedListener {
    private final String TAG = "RecorderActivity";
    private final long DEFAULT_TIMER = 1000 * 60 * 2;
    private final String DEFAULT_ACTIVITY_TYPE = "standing";

    private long timer;
    private volatile boolean stopTimer = false;
    private String activityType = DEFAULT_ACTIVITY_TYPE;

    private Button startRecordingButton;
    private EditText timerEditText;
    private EditText urlEditText;
    private EditText fileIdEditText;
    private Spinner activityTypeSpinner;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recorder);

        this.setupReference();
        this.setupActivityTypeSpinnerListener();

        this.loadTimerPreferences();
        this.loadURLPreferences();
        this.loadFileIdPreferences();
    }

    private void setupReference() {
        this.startRecordingButton = (Button) this.findViewById(R.id.start_recording_button);
        this.timerEditText = (EditText) this.findViewById(R.id.timer_edittext);
        this.urlEditText = (EditText) this.findViewById(R.id.url_edittext);
        this.fileIdEditText = (EditText) this.findViewById(R.id.file_id_edittext);
        this.activityTypeSpinner = (Spinner) this.findViewById(R.id.activity_type_spinner);
    }

    private void setupActivityTypeSpinnerListener() {
        this.activityTypeSpinner.setOnItemSelectedListener(this);
    }

    private void loadTimerPreferences() {
        this.timer = SharedPreferencesController.getInstance().getLong(SharedPreferencesKey.TIMER_KEY);
        if (this.timer == 0) this.timer = DEFAULT_TIMER;
        this.timerEditText.setText("" + this.timer / 1000);
    }

    private void loadURLPreferences() {
        String ngrokId = UrlController.getInstance().getNgrokId();
        this.urlEditText.setText(ngrokId);
    }

    private void loadFileIdPreferences() {
        long fileId = SharedPreferencesController.getInstance().getInt(SharedPreferencesKey.FILE_ID_KEY);
        this.fileIdEditText.setText("" + fileId);
    }

    private class Timer extends AsyncTask<Void, Void, Void> {
        @Override
        protected Void doInBackground(Void... params) {
            long start = System.currentTimeMillis();
            long diff;

            while (!stopTimer) {
                diff = System.currentTimeMillis() - start;
                if (diff >= timer) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            stopSensorRecording();
                        }
                    });

                    // Because the runnable action is queued if the current thread is not the UI thread
                    stopTimer = true;
                } else {
                    try {
                        Thread.sleep(2000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }

            return null;
        }
    }

    public void startSensorRecording(View view) {
        SensorController.getInstance().startSmartwatchSensorRecording(activityType);
        this.stopTimer = false;
        new Timer().execute();

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

        Toast.makeText(this, "Start sensor recording!", Toast.LENGTH_SHORT).show();
        this.startSensorRecordingRingtone();
        this.startRecordingButton.setEnabled(false);
    }

    private void startSensorRecordingRingtone() {
        AudioUtil.play(this, R.raw.beep);
    }

    public void stopSensorRecording(View view) {
        this.stopSensorRecording();
    }

    private void stopSensorRecording() {
        SensorController.getInstance().stopSmartwatchSensorRecording();

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

        Toast.makeText(this, "Stop sensor recording!", Toast.LENGTH_SHORT).show();
        this.stopTimer = true;
        this.stopSensorRecordingRingtone();
        this.startRecordingButton.setEnabled(true);
    }

    private void stopSensorRecordingRingtone() {
        try {
            AudioUtil.play(this, R.raw.beep);
            Thread.sleep(500);
            AudioUtil.play(this, R.raw.beep);
            Thread.sleep(500);
            AudioUtil.play(this, R.raw.beep);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void saveTimer(View view) {
        try {
            this.timer = Long.parseLong(this.timerEditText.getText().toString()) * 1000;
            SharedPreferencesController.getInstance().setLong(SharedPreferencesKey.TIMER_KEY, this.timer);
        } catch (NumberFormatException e) {
            this.timer = DEFAULT_TIMER;
        } finally {
            long timerInSecond = this.timer / 1000;
            Toast.makeText(this, "Timer: " + timerInSecond + "s", Toast.LENGTH_SHORT).show();
        }
    }

    public void saveURL(View v) {
        String url = this.urlEditText.getText().toString();
        UrlController.getInstance().setServerAddress(url);
        SharedPreferencesController.getInstance().setString(SharedPreferencesKey.SERVER_URL_KEY, URL.SERVER_ADDRESS);
    }

    public void saveFileId(View v) {
        String fileIdString = this.fileIdEditText.getText().toString();
        try {
            int fileId = Integer.parseInt(fileIdString);
            FileIdController.getInstance().setFileId(fileId);
        } catch (NumberFormatException e) {
            e.printStackTrace();
        }
    }

    public void sendFileToServer(View view) {
        final Response.Listener<JSONObject> onSuccess = new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Toast.makeText(RecorderActivity.this, "Sent to server!", Toast.LENGTH_SHORT).show();
            }
        };

        final Response.ErrorListener onError = new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(RecorderActivity.this, "Cannot send to server!", Toast.LENGTH_SHORT).show();
            }
        };

        final ProgressDialog progressDialog = ProgressDialog.show(this, "Loading..", "Sending sensor data to server..", true);
        new Thread(new Runnable() {
            @Override
            public void run() {
                SensorController.getInstance().sendSensoryData(RecorderActivity.this, activityType, onSuccess, onError);
                progressDialog.dismiss();
            }
        }).start();
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        this.activityType = (String) parent.getItemAtPosition(position);
        this.activityType = this.activityType.replaceAll(" ", "_").toLowerCase();
        Log.i(TAG, this.activityType);
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {}
}
