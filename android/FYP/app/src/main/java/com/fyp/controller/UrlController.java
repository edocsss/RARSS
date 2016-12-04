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
        this.setServerAddress(this.getNgrokId());
    }

    public String getNgrokId() {
        String serverUrl = SharedPreferencesController.getInstance().getString(SharedPreferencesKey.SERVER_URL_KEY);
        if (!serverUrl.isEmpty()) {
            int lastSlashPos = serverUrl.indexOf("/") + 1;
            int firstDotPos = serverUrl.indexOf(".");

            return serverUrl.substring(lastSlashPos + 1, firstDotPos);
        } else {
            return "";
        }
    }

    public void setServerAddress(String ngrokId) {
        URL.SERVER_ADDRESS = "http://" + ngrokId + ".ngrok.io";
        URL.SEND_SENSORY_DATA_ADDRESS = URL.SERVER_ADDRESS;
        URL.NOTIFY_SMARTWATCH_ADDRESS = URL.SERVER_ADDRESS + "/smartwatch/notify";
    }
}
