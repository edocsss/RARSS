package com.fyp.util;

import android.content.Context;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class FileUtil {
    public static void writeFile(Context context, String fileName, byte[] data) {
        try {
            FileOutputStream fos = context.openFileOutput(fileName, Context.MODE_PRIVATE);
            fos.write(data);
            fos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String readFile(Context context, String fileName) {
        int n;
        StringBuffer sb = new StringBuffer();
        byte[] buffer = new byte[1024];

        try {
            FileInputStream fis = context.openFileInput(fileName);
            while ((n = fis.read(buffer)) != -1) {
                sb.append(new String(buffer, 0, n));
            }

            return sb.toString();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
