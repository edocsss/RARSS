package com.fyp.controller;

import com.fyp.constant.SharedPreferencesKey;
import com.fyp.constant.URL;

public class UrlController {
    private static UrlController instance = null;

    public static UrlController getInstance() {
        if (instance == null) {
            instance = new UrlController();
        }

        return instance;
    }

    public void initUrl() {
        this.setServerAddress(this.getTunnelId());
    }

    public String getTunnelId() {
        String serverUrl = SharedPreferencesController.getInstance().getString(SharedPreferencesKey.SERVER_URL_KEY);
        if (!serverUrl.isEmpty()) {
            int lastSlashPos = serverUrl.indexOf("/") + 1;
            int firstDotPos = serverUrl.indexOf(".");

            return serverUrl.substring(lastSlashPos + 1, firstDotPos);
        } else {
            return "";
        }
    }

    public void setServerAddress(String tunnelId) {
        URL.SERVER_ADDRESS = "http://" + tunnelId + ".ngrok.io";
        URL.SEND_SENSORY_DATA_RECORDING_ADDRESS = URL.SERVER_ADDRESS + "/smartphone/recording";
        URL.SEND_SENSORY_DATA_MONITORING_ADDRESS = URL.SERVER_ADDRESS + "/smartphone/monitoring";
        URL.NOTIFY_SMARTWATCH_RECORDING_ADDRESS = URL.SERVER_ADDRESS + "/smartwatch/recording/notify";
        URL.NOTIFY_SMARTWATCH_MONITORING_ADDRESS = URL.SERVER_ADDRESS + "/smartwatch/monitoring/notify";
    }
}
