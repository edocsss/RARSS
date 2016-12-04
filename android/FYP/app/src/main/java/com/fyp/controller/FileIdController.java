package com.fyp.controller;

import com.fyp.constant.SharedPreferencesKey;

public class FileIdController {
    private static FileIdController instance = null;

    public static FileIdController getInstance() {
        if (instance == null) {
            instance = new FileIdController();
        }

        return instance;
    }

    public void initFileId() {
        if (SharedPreferencesController.getInstance().getInt(SharedPreferencesKey.FILE_ID_KEY) == 0) {
            SharedPreferencesController.getInstance().setInt(SharedPreferencesKey.FILE_ID_KEY, 70);
        }
    }

    public int getNextFileIdAndIncrement() {
        int nextFileId = SharedPreferencesController.getInstance().getInt(SharedPreferencesKey.FILE_ID_KEY);
        SharedPreferencesController.getInstance().setInt(SharedPreferencesKey.FILE_ID_KEY, nextFileId + 1);
        return nextFileId;
    }

    public void setFileId(int fileId) {
        SharedPreferencesController.getInstance().setInt(SharedPreferencesKey.FILE_ID_KEY, fileId);
    }
}
