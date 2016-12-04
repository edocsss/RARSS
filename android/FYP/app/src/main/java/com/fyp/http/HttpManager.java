package com.fyp.http;

import android.content.Context;
import android.util.Log;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.fyp.FYPApp;
import com.fyp.constant.HttpConfig;

import org.json.JSONObject;

public class HttpManager {
    private static String TAG = "HTTPManager";
    private static HttpManager instance = null;
    private static Context context;
    private static RequestQueue requestQueue;

    private HttpManager () {
        requestQueue = Volley.newRequestQueue(context);
    }

    public static HttpManager getInstance () {
        if (instance == null) instance = new HttpManager();
        return instance;
    }

    public static void init(Context c) {
        context = c;
    }

    private boolean enqueueRequest(Request request) {
        try {
            requestQueue.add(request);
            return true;
        } catch (Exception e) {
            Log.e(TAG, e.toString());
            return false;
        }
    }

    public void sendPostRequest(final JSONObject jsonObject,
                                final String url,
                                Response.Listener<JSONObject> onSuccess,
                                Response.ErrorListener onError) {
        JsonObjectRequest postRequest = new JsonObjectRequest(
                Request.Method.POST,
                url,
                jsonObject,
                onSuccess,
                onError
        );

        postRequest.setRetryPolicy(new DefaultRetryPolicy(
                HttpConfig.REQUEST_TIMEOUT,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        HttpManager.getInstance().enqueueRequest(postRequest);
    }
}
