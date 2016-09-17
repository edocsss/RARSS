package com.fyp.controller;

import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.fyp.FYPApp;
import com.fyp.constant.URL;
import com.fyp.http.HttpManager;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class SensorController {
    private static String TAG = "SensorController";
    private List<Sensor> availableSensors;
    private SensorManager sensorManager;
    private static SensorController instance = null;

    public SensorController(SensorManager sensorManager) {
        this.availableSensors = new ArrayList<>();
        this.sensorManager = sensorManager;
    }

    public static SensorController getInstance() {
        if (instance == null) {
            instance = new SensorController(FYPApp.getSensorManager());
        }

        return instance;
    }

    public List<Sensor> getAvailableSensors() {
        return availableSensors;
    }

    public void detectAllAvailableSensors() {
        Log.i(TAG, "Retrieving all available sensors on this device...");
        this.availableSensors = this.sensorManager.getSensorList(Sensor.TYPE_ALL);
        Log.i(TAG, "All available sensors are retrieved!");
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
