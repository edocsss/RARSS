package com.fyp.activity;

import android.graphics.Typeface;
import android.hardware.Sensor;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.fyp.R;
import com.fyp.controller.SensorController;

import java.util.List;

import static android.view.ViewGroup.LayoutParams.MATCH_PARENT;
import static android.view.ViewGroup.LayoutParams.WRAP_CONTENT;

public class SensorDetailsActivity extends AppCompatActivity {
    private final String TAG = "SensorDetailsActivity";
    private int MARGIN;
    private LinearLayout sensorDetailsContainer;
    private List<Sensor> availableSensors;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sensor_details);

        this.setupReference();
        this.displaySensorDetails();
    }

    private void setupReference() {
        this.sensorDetailsContainer = (LinearLayout) this.findViewById(R.id.sensor_details_container);
        this.availableSensors = SensorController.getInstance().getAvailableSensors();
        this.MARGIN = (int) this.getResources().getDimension(R.dimen.margin_sm);
    }


    private void displaySensorDetails() {
        for (Sensor s: this.availableSensors) {
            LinearLayout ll = new LinearLayout(this);
            TextView tv = new TextView(this);

            LinearLayout.LayoutParams llLayoutParams = new LinearLayout.LayoutParams(MATCH_PARENT, WRAP_CONTENT);
            llLayoutParams.setMargins(0, MARGIN, 0, MARGIN);
            ll.setLayoutParams(llLayoutParams);
            ll.setOrientation(LinearLayout.VERTICAL);

            ll.addView(this.getSensorDetailsChildLayout("Max. Range", "" + s.getMaximumRange()));
            ll.addView(this.getSensorDetailsChildLayout("Min. Delay", "" + s.getMinDelay()));
            ll.addView(this.getSensorDetailsChildLayout("Name", s.getName()));
            ll.addView(this.getSensorDetailsChildLayout("Power", "" + s.getPower()));
            ll.addView(this.getSensorDetailsChildLayout("Resolution", "" + s.getResolution()));
            ll.addView(this.getSensorDetailsChildLayout("Vendor", s.getVendor()));
            ll.addView(this.getSensorDetailsChildLayout("Version", "" + s.getVersion()));
            this.sensorDetailsContainer.addView(ll);
        }

    }

    private LinearLayout getSensorDetailsChildLayout(String header, String content) {
        LinearLayout ll = new LinearLayout(this);
        TextView tvHeader = new TextView(this);
        TextView tvContent = new TextView(this);

        LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(MATCH_PARENT, WRAP_CONTENT);
        ll.setLayoutParams(layoutParams);
        ll.setOrientation(LinearLayout.HORIZONTAL);

        LinearLayout.LayoutParams headerLayoutParams = new LinearLayout.LayoutParams(WRAP_CONTENT, WRAP_CONTENT);
        headerLayoutParams.setMargins(0, 0, MARGIN, 0);

        tvHeader.setText(header);
        tvHeader.setTypeface(null, Typeface.BOLD);
        tvHeader.setLayoutParams(headerLayoutParams);
        tvContent.setText(content);

        ll.addView(tvHeader);
        ll.addView(tvContent);

        return ll;
    }
}