package com.fyp.util;

import android.app.ProgressDialog;
import android.content.Context;
import android.media.MediaPlayer;

import com.fyp.R;

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

    public static void playStopRecordingRingtone(Context c) {
        try {
            AudioUtil.play(c, R.raw.beep);
            Thread.sleep(500);
            AudioUtil.play(c, R.raw.beep);
            Thread.sleep(500);
            AudioUtil.play(c, R.raw.beep);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void playStartRecordingRingtone(Context c) {
        AudioUtil.play(c, R.raw.beep);
    }
}
