package com.fyp.june.trackingsystem;
//http://www.websmithing.com/2011/02/01/how-to-update-the-ui-in-an-android-activity-using-data-from-a-background-service/
import java.text.SimpleDateFormat;
import java.util.Date;

import com.fyp.june.trackingsystem.MainActivity.CountDownRunner;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

public class MainService extends Service implements SensorEventListener {

	private Handler proximityTvHandler, accelerometerTvHandler, lightHandler, amTempHandler, barometerHandler;
	private Handler locHandler, gyroHandler, magHandler;
	private SensorManager mSensorManager;
	private Sensor mProximity, mAccelerometer, mLight, mAmTemp, mGyro, mMag, mBarometer;
	
	/**
	 * For gyroscope
	 */
	private static final float NS2S = 1.0f / 1000000000.0f;
    private final float[] deltaRotationVector = new float[4];
    private float timestamp;
    private static final float EPSILON = 0.000000001f;
    
    final float[] mValuesMagnet      = new float[3];
    final float[] mValuesAccel       = new float[3];
    final float[] mValuesOrientation = new float[3];
    final float[] mRotationMatrix    = new float[9];
    final float[] mValueBarometer = new float[1];
	
	@Override
	public IBinder onBind(Intent arg0) {
		// TODO Auto-generated method stub
		return null;
	}
	
	private static final String TAG = "BroadcastService";
    public static final String BROADCAST_ACTION = "com.fyp.june.trackingsystem.MainService.displayevent";
    private final Handler handler = new Handler();
    Intent intent;
    int counter = 0;
	
    @Override
    public void onCreate() {
        super.onCreate();
    	intent = new Intent(BROADCAST_ACTION);	
    //	Toast.makeText(getApplicationContext(), "Service Started", Toast.LENGTH_LONG).show();
    	proximityTvHandler = new Handler();
		accelerometerTvHandler = new Handler();
		lightHandler = new Handler();
		amTempHandler = new Handler();
		locHandler = new Handler();
		gyroHandler = new Handler();
		magHandler = new Handler();
		barometerHandler = new Handler();
		
		
		
		
		/**
		 * To track the location via GPS, but battery drain too much, so remove it first
		 */
		LocationManager locationManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);

		// Define a listener that responds to location updates
		LocationListener locationListener = new LocationListener() {
		    public void onStatusChanged(String provider, int status, Bundle extras) {}
		    public void onProviderEnabled(String provider) {}
		    public void onProviderDisabled(String provider) {}

			@Override
			public void onLocationChanged(Location location) {
				String acc = Float.toString(location.getAccuracy());
				double lat = location.getLatitude();
				double longitude = location.getLongitude();
				// TODO Auto-generated method stub
				//makeUseOfNewLocation(location);
				//locTv.setText("Accuracy: " + acc + " \nLatitude: " + lat + " \nLongitude: " + longitude);
				
			}
		  };

		// Register the listener with the Location Manager to receive location updates
		//locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListener);
	
		Thread myThread = null;

		Runnable myRunnableThread = new CountDownRunner();
		myThread= new Thread(myRunnableThread);   
		myThread.start();   

		// Get an instance of the sensor service, and use that to get an instance of
		// a particular sensor.
		mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
		mProximity = mSensorManager.getDefaultSensor(Sensor.TYPE_PROXIMITY);
		mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
		mAmTemp = mSensorManager.getDefaultSensor(Sensor.TYPE_AMBIENT_TEMPERATURE);
		mLight = mSensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
		mMag = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
		mGyro = mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
		mBarometer = mSensorManager.getDefaultSensor(Sensor.TYPE_PRESSURE);
		
		
		mSensorManager.registerListener(this, mProximity, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mAmTemp, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mMag, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mLight, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mGyro, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mBarometer, SensorManager.SENSOR_DELAY_NORMAL);

    }
    

	class CountDownRunner implements Runnable{
		// @Override
		public void run() {
			while(!Thread.currentThread().isInterrupted()){
				try {
					Thread.sleep(1000); // Pause of 1 Second
				} catch (InterruptedException e) {
					Thread.currentThread().interrupt();
				}catch(Exception e){
				}
			}
		}
	}
    
	
	/**
	 * Application to display sensors information whenever sensor event changed
	 * Sensors: Proximity, accelerometer, ambient temp, ambient light
	 */
	public void onSensorChanged(SensorEvent event) {
		//Toast.makeText(getApplicationContext(), "Service Startedzzz", Toast.LENGTH_SHORT).show();

		if(event.sensor.getType()==Sensor.TYPE_PROXIMITY){
			final String distance = Float.toString(event.values[0]);
			proximityTvHandler.post(new Runnable() {
				@Override
				public void run() {
					//Toast.makeText(getApplicationContext(), distance + "cm", Toast.LENGTH_LONG).show();
					//proximityTv.setText(" " + distance + "cm");
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_ACCELEROMETER){
			float accX = event.values[0];
			float accY = event.values[1];
			float accZ = event.values[2];
			final String sAccX = String.format("%.3f", accX);
			final String sAccY = String.format("%.3f", accY);
			final String sAccZ = String.format("%.3f", accZ);
			
			final float alpha = (float) 0.8;
			
			final float[] gravity;
			gravity = new float[10];
			
			final float[] linear_acceleration;
			linear_acceleration = new float[10];

	        gravity[0] = alpha * gravity[0] + (1 - alpha) * event.values[0];
	        gravity[1] = alpha * gravity[1] + (1 - alpha) * event.values[1];
	        gravity[2] = alpha * gravity[2] + (1 - alpha) * event.values[2];

	        linear_acceleration[0] = event.values[0] - gravity[0];
	        linear_acceleration[1] = event.values[1] - gravity[1];
	        linear_acceleration[2] = event.values[2] - gravity[2];
	        
	        final String sGravityX = String.format("%.3f", gravity[0]);
			final String sGravityY = String.format("%.3f", gravity[1]);
			final String sGravityZ = String.format("%.3f", gravity[2]);
			
			final String slinearAccX = String.format("%.3f", linear_acceleration[0]);
			final String slinearAccY = String.format("%.3f", linear_acceleration[1]);
			final String slinearAccZ = String.format("%.3f", linear_acceleration[2]);
			
			/**
			 * The following methods are for finding gyroscope sensor values
			 */
			System.arraycopy(event.values, 0, mValuesAccel, 0, 3);
			SensorManager.getRotationMatrix(mRotationMatrix, null, mValuesAccel, mValuesMagnet);
            SensorManager.getOrientation(mRotationMatrix, mValuesOrientation);
            final CharSequence test;
                        
            final String sGyroX = String.format("%.3f", mValuesOrientation[0]);
			final String sGyroY = String.format("%.3f", mValuesOrientation[1]);
			final String sGyroZ = String.format("%.3f", mValuesOrientation[2]);
			//orientMat[0]*180/(float)Math.PI
			test = "x =" + sGyroX +"rad y = "+ sGyroY + "rad z = "+ sGyroZ + "rad";
            
            // txt1.setText(test);
			accelerometerTvHandler.post(new Runnable() {
				@Override
				public void run() {
					//Toast.makeText(getApplicationContext(), " x = " + sAccX + "m/s²  y = " + sAccY + "m/s²   z = " + sAccZ +"m/s²", Toast.LENGTH_SHORT).show();
//					accelerometerTv.setText(" x = " + sAccX + "m/s²  y = " + sAccY + "m/s²   z = " + sAccZ +"m/s²");
//					gravityTv.setText(" x = " + sGravityX + "m/s²  y = " + sGravityY + "m/s²   z = " + sGravityZ +"m/s²");
//					linearAccTv.setText(" x = " + slinearAccX + "m/s²  y = " + slinearAccY + "m/s²   z = " + slinearAccZ +"m/s²");
//					gyroTv.setText(test);
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_AMBIENT_TEMPERATURE){
			float temp = event.values[0];
			final String sTemp = String.format("%.3f", temp);
			
			amTempHandler.post(new Runnable() {
				@Override
				public void run() {
					//amTempTv.setText(" " + sTemp + "°C");
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_MAGNETIC_FIELD){
			float magX = event.values[0];
			float magY = event.values[1];
			float magZ = event.values[2];
			final String sMagX = String.format("%.3f", magX);
			final String sMagY = String.format("%.3f", magY);
			final String sMagZ = String.format("%.3f", magZ);
			
			System.arraycopy(event.values, 0, mValuesMagnet, 0, 3);
			
			magHandler.post(new Runnable() {
				@Override
				public void run() {
					//magTv.setText(" x = " + sMagX + "uT  y = " + sMagY + "uT  z =" + sMagZ + "uT");
				}
			});
		}
		
		else if (event.sensor.getType()==Sensor.TYPE_PRESSURE){
			float barometer = event.values[0];
			final String sBarometer = String.format("%.3f", barometer);
			System.arraycopy(event.values, 0, mValueBarometer, 0, 1);
			barometerHandler.post(new Runnable(){
				@Override
				public void run() {
					
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_LIGHT){
			float light = event.values[0];
			final String sLight = String.format("%.3f", light);
			
			lightHandler.post(new Runnable() {
				@Override
				public void run() {
					//lightTv.setText(" " + sLight + "lx");
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_GYROSCOPE){
			
			SensorManager.getRotationMatrix(mRotationMatrix, null, mValuesAccel, mValuesMagnet);
            SensorManager.getOrientation(mRotationMatrix, mValuesOrientation);
			
//			// This timestep's delta rotation to be multiplied by the current rotation
//	        // after computing it from the gyro sample data.
//	        if (timestamp != 0) {
//	            final float dT = (event.timestamp - timestamp) * NS2S;
//	            // Axis of the rotation sample, not normalized yet.
//	            float axisX = event.values[0];
//	            float axisY = event.values[1];
//	            float axisZ = event.values[2];
//
//	            // Calculate the angular speed of the sample
//	            float omegaMagnitude = (float) Math.sqrt(axisX*axisX + axisY*axisY + axisZ*axisZ);
//
//	            // Normalize the rotation vector if it's big enough to get the axis
//	            if (omegaMagnitude > EPSILON) {
//	                axisX /= omegaMagnitude;
//	                axisY /= omegaMagnitude;
//	                axisZ /= omegaMagnitude;
//	            }
//
//	            // Integrate around this axis with the angular speed by the timestep
//	            // in order to get a delta rotation from this sample over the timestep
//	            // We will convert this axis-angle representation of the delta rotation
//	            // into a quaternion before turning it into the rotation matrix.
//	            float thetaOverTwo = omegaMagnitude * dT / 2.0f;
//	            float sinThetaOverTwo = (float)Math.sin(thetaOverTwo);
//	            float cosThetaOverTwo = (float)Math.cos(thetaOverTwo);
//	            deltaRotationVector[0] = sinThetaOverTwo * axisX;
//	            deltaRotationVector[1] = sinThetaOverTwo * axisY;
//	            deltaRotationVector[2] = sinThetaOverTwo * axisZ;
//	            deltaRotationVector[3] = cosThetaOverTwo;
//	          }
//		        timestamp = event.timestamp;
//		        final float[] deltaRotationMatrix = new float[9];
//		        //get current rotation
//		        SensorManager.getRotationMatrix(deltaRotationMatrix, deltaRotationVector);
//		        // User code should concatenate the delta rotation we computed with the current rotation
//		        // in order to get the updated rotation.
//		        gravity = gravity * deltaRotationMatrix;
//		         //rotationCurrent = rotationCurrent * deltaRotationMatrix;
//		        //SensorManager.getOrientation(deltaRotationMatrix, deltaRotationVector);
//		        final String r1 = String.format("%.1f", deltaRotationMatrix[0]);
//		        final String r2 = String.format("%.1f", deltaRotationMatrix[1]);
//		        final String r3 = String.format("%.1f", deltaRotationMatrix[2]);
//		        
//			gyroHandler.post(new Runnable() {
//				@Override
//				public void run() {
//					gyroTv.setText(" x = " + r1 + "rad/s    y = " +  r2 + "rad/s    z = " + r3 + "rad/s");
//				}
//			});
		}

	}
	
	protected void onResume() {
		// Register a listener for the sensor.
		//super.onResume();
		mSensorManager.registerListener(this, mProximity, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mAmTemp, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mMag, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mLight, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mGyro, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mBarometer, SensorManager.SENSOR_DELAY_NORMAL);
	}
	
	public void setListeners(SensorManager sensorManager, SensorEventListener mEventListener)
    {
        sensorManager.registerListener(mEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), 
                SensorManager.SENSOR_DELAY_NORMAL);
        sensorManager.registerListener(mEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD), 
                SensorManager.SENSOR_DELAY_NORMAL);
        sensorManager.registerListener(mEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_PRESSURE), 
                SensorManager.SENSOR_DELAY_NORMAL);
    }
	
    @Override
    public void onStart(Intent intent, int startId) {
        handler.removeCallbacks(sendUpdatesToUI);
        handler.postDelayed(sendUpdatesToUI, 1000); // 1 second
        //Toast.makeText(getApplicationContext(), "Service Started", Toast.LENGTH_LONG).show();
        
    }
    
    private Runnable sendUpdatesToUI = new Runnable() {
    	public void run() {
    	    DisplayLoggingInfo();    		
    	    handler.postDelayed(this, 5000); // 5 seconds
    	}
    };
    
    private void DisplayLoggingInfo() {
    	Log.d(TAG, "entered DisplayLoggingInfo");
 
    	intent.putExtra("time", new Date().toString());
    	intent.putExtra("counter", String.valueOf(++counter));
    	sendBroadcast(intent);
    }

	@Override
	public void onAccuracyChanged(Sensor arg0, int arg1) {
		// TODO Auto-generated method stub
		
	}
}
