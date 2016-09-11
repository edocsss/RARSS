package com.fyp.util;

import android.app.ProgressDialog;
import android.content.Context;
import android.media.MediaPlayer;

public class AudioUtil {
    private static MediaPlayer mediaPlayer;

    public static void stop() {
        if (mediaPlayer != null) {
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }

    public static void play(Context c, int rid) {
        stop();

        mediaPlayer = MediaPlayer.create(c, rid);
        mediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
            @Override
            public void onCompletion(MediaPlayer mp) {
                stop();
            }
        });

        mediaPlayer.start();
    }
}
