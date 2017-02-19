package com.fyp.task;

import com.fyp.controller.RealTimeMonitoringController;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.UUID;

public class RealTimeMonitoringDataHandler implements Runnable {
    private String accelerometerReadingsString;
    private String gyroscopeReadingsString;
    private String barometerReadingsString;

    public RealTimeMonitoringDataHandler(
            String accelerometerReadingsString,
            String gyroscopeReadingsString,
            String barometerReadingsString
    ) {
        this.accelerometerReadingsString= accelerometerReadingsString;
        this.gyroscopeReadingsString = gyroscopeReadingsString;
        this.barometerReadingsString = barometerReadingsString;
    }

    @Override
    public void run() {
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("uuid", UUID.randomUUID());
            jsonObject.put("sp_accelerometer", this.accelerometerReadingsString);
            jsonObject.put("sp_gyroscope", this.gyroscopeReadingsString);
            jsonObject.put("sp_barometer", this.barometerReadingsString);
            RealTimeMonitoringController.getInstance().handleRealTimeData(jsonObject);
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
}
