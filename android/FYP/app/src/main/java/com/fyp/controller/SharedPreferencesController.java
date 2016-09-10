package com.fyp.controller;

import android.content.Context;
import android.content.SharedPreferences;

import com.fyp.FYPApp;

public class SharedPreferencesController {
    private final String SHARED_PREFERENCES_NAME = "FYPApp";
    private SharedPreferences sharedPreferences;
    private static SharedPreferencesController instance = null;

    public SharedPreferencesController(Context context) {
        this.sharedPreferences = context.getSharedPreferences(SHARED_PREFERENCES_NAME, Context.MODE_PRIVATE);
    }

    public static SharedPreferencesController getInstance() {
        if (instance == null) {
            instance = new SharedPreferencesController(FYPApp.getContext());
        }

        return instance;
    }

    public void setLong(String key, long value) {
        SharedPreferences.Editor editor = this.sharedPreferences.edit();
        editor.putLong(key, value);
        editor.apply();
    }

    public long getLong(String key) {
        return this.sharedPreferences.getLong(key, 0);
    }

    public void setString(String key, String value) {
        SharedPreferences.Editor editor = this.sharedPreferences.edit();
        editor.putString(key, value);
        editor.apply();
    }

    public String getString(String key) {
        return this.sharedPreferences.getString(key, "");
    }
}
