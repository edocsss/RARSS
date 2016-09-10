package com.fyp.http;

import android.content.Context;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.fyp.FYPApp;
import com.fyp.constant.URL;

import org.json.JSONException;
import org.json.JSONObject;

public class HttpManager {
    private static String TAG = "HTTPManager";
    public static final int POST_REQUEST_TIMEOUT = 60000; // 1 minute
    public static final int POST_REQUEST_MAX_RETRY = 2;

    private static HttpManager instance = null;
    private static RequestQueue requestQueue;

    private HttpManager (Context context) {
        requestQueue = Volley.newRequestQueue(context);
    }

    public static HttpManager getInstance () {
        if (instance == null) instance = new HttpManager(FYPApp.getContext());
        return instance;
    }

    public boolean enqueueRequest(Request request) {
        try {
            requestQueue.add(request);
            return true;
        } catch (Exception e) {
            Log.e(TAG, e.toString());
            return false;
        }
    }

    public void cancelAllRequests() {
        requestQueue.cancelAll(new RequestQueue.RequestFilter() {
            @Override
            public boolean apply(Request<?> request) {
                return true;
            }
        });
    }

    public void cancelAllRequestsByTag (String requestTag) {
        requestQueue.cancelAll(requestTag);
    }

    public void sendFileContent(final String activityType,
                                final String fileName,
                                final String fileContent,
                                Response.Listener<JSONObject> onSuccess,
                                Response.ErrorListener onError) {

        JSONObject sendFileJSON = new JSONObject();
        try {
            sendFileJSON.put("activityType", activityType);
            sendFileJSON.put("fileName", fileName);
            sendFileJSON.put("fileContent", fileContent);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest sendFileRequest = new JsonObjectRequest(
                Request.Method.POST,
                URL.SERVER_ADDRESS,
                sendFileJSON,
                onSuccess,
                onError
        );

        HttpManager.getInstance().enqueueRequest(sendFileRequest);
    }
}
