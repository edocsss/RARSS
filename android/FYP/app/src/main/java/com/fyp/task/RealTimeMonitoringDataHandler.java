package com.fyp.task;

import com.fyp.controller.RealTimeMonitoringController;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.UUID;

public class RealTimeMonitoringDataHandler implements Runnable {
    private String accelerometerReadingsString;

    public RealTimeMonitoringDataHandler(String accelerometerReadingsString) {
        this.accelerometerReadingsString= accelerometerReadingsString;
    }

    @Override
    public void run() {
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("uuid", UUID.randomUUID());
            jsonObject.put("sp_accelerometer", this.accelerometerReadingsString);
            RealTimeMonitoringController.getInstance().handleRealTimeData(jsonObject);
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
}
