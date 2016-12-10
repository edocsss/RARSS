package com.fyp.controller;

import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.fyp.constant.URL;
import com.fyp.http.HttpManager;

import org.json.JSONException;
import org.json.JSONObject;

public class RealTimeMonitoringController {
    private final String TAG = "RTMController";
    private static RealTimeMonitoringController instance = null;

    public static RealTimeMonitoringController getInstance() {
        if (instance == null) {
            instance = new RealTimeMonitoringController();
        }

        return instance;
    }

    public void handleRealTimeData(JSONObject jsonObject) {
        HttpManager.getInstance().sendPostRequest(jsonObject, URL.SEND_SENSORY_DATA_MONITORING_ADDRESS, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Log.i(TAG, "Real Time data sent!");
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e(TAG, "Error during sending real time data!");
                Log.e(TAG, error.toString());
            }
        });
    }

    private void notifySmartwatchSensorMonitoring(boolean start) {
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("start", start);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        HttpManager.getInstance().sendPostRequest(
                jsonObject,
                URL.NOTIFY_SMARTWATCH_MONITORING_ADDRESS,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e(TAG, error.toString());
                    }
                }
        );
    }

    public void startSmartwatchSensorMonitoring() {
        notifySmartwatchSensorMonitoring(true);
    }

    public void stopSmartwatchSensorMonitoring() {
        notifySmartwatchSensorMonitoring(false);
    }
}