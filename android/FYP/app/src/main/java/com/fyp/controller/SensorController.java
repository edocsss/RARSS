package com.fyp.controller;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.fyp.FYPApp;
import com.fyp.constant.FileNames;
import com.fyp.constant.URL;
import com.fyp.http.HttpManager;
import com.fyp.util.FileUtil;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class SensorController {
    private static String TAG = "SensorController";
    private List<Sensor> availableSensors;
    private SensorManager sensorManager;
    private static SensorController instance = null;

    private SensorController(SensorManager s) {
        this.availableSensors = new ArrayList<>();
        this.sensorManager = s;
    }

    public static SensorController getInstance() {
        if (instance == null) {
            instance = new SensorController(FYPApp.getSensorManager());
        }

        return instance;
    }

    public List<Sensor> getAvailableSensors() {
        return this.availableSensors;
    }

    public void detectAllAvailableSensors() {
        Log.i(TAG, "Retrieving all available sensors on this device...");
        this.availableSensors = sensorManager.getSensorList(Sensor.TYPE_ALL);
        Log.i(TAG, "All available sensors are retrieved!");
    }

    public void sendSensoryData(Context c, String activityType, Response.Listener<JSONObject> onSuccess, Response.ErrorListener onError) {
        JSONObject jsonObject = new JSONObject();
        JSONObject sensoryData = new JSONObject();

        try {
            String accelerometerResultFileContent = FileUtil.readFile(c, FileNames.ACCELEROMETER_RESULT);
            String barometerResultFileContent = FileUtil.readFile(c, FileNames.BAROMETER_RESULT);
            String gravityResultFileContent = FileUtil.readFile(c, FileNames.GRAVITY_RESULT);
            String gyroscopeResultFileContent = FileUtil.readFile(c, FileNames.GYROSCOPE_RESULT);
            String linearAccelerometerResultFileContent = FileUtil.readFile(c, FileNames.LINEAR_ACCELEROMETER_RESULT);
            String magneticResultFileContent = FileUtil.readFile(c, FileNames.MAGNETIC_RESULT);

            sensoryData.put("accelerometer", accelerometerResultFileContent);
            sensoryData.put("barometer", barometerResultFileContent);
            sensoryData.put("gravity", gravityResultFileContent);
            sensoryData.put("gyroscope", gyroscopeResultFileContent);
            sensoryData.put("linearAccelerometer", linearAccelerometerResultFileContent);
            sensoryData.put("magnetic", magneticResultFileContent);
            
            jsonObject.put("activityType", activityType);
            jsonObject.put("sensoryData", sensoryData);
            jsonObject.put("fileId", FileIdController.getInstance().getNextFileIdAndIncrement());
        } catch (JSONException e) {
            e.printStackTrace();
        }

        HttpManager.getInstance().sendPostRequest(jsonObject, URL.SEND_SENSORY_DATA_ADDRESS, onSuccess, onError);
    }

    public void startSmartwatchSensorRecording(String activityType) {
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("start", true);
            jsonObject.put("activityType", activityType);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        HttpManager.getInstance().sendPostRequest(
                jsonObject,
                URL.NOTIFY_SMARTWATCH_ADDRESS,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e(TAG, error.getMessage());
                    }
                }
        );
    }

    public void stopSmartwatchSensorRecording() {
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("start", false);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        HttpManager.getInstance().sendPostRequest(
                jsonObject,
                URL.NOTIFY_SMARTWATCH_ADDRESS,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                    }
                }
        );
    }
}
