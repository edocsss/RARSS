package com.fyp.june.trackingsystem;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;

import com.db4o.config.TVector;
import com.fyp.june.entities.AccelerometerDetails;
import com.fyp.june.entities.ActivityTagged;
import com.fyp.june.entities.AmbientLightDetails;
import com.fyp.june.entities.BarometerDetails;
import com.fyp.june.entities.ClientToServerContainer;
import com.fyp.june.entities.GyroscopeDetails;
import com.fyp.june.entities.LinearAccDetails;
import com.fyp.june.entities.MagneticFieldDetails;
import com.fyp.june.utilities.DeviceUuidFactory;
import com.fyp.june.utilities.HTTPHandler;
import com.fyp.june.utilities.HTTPHandler.OnResponseReceivedListener;
import com.github.julman99.gsonfire.DateSerializationPolicy;
import com.github.julman99.gsonfire.GsonFireBuilder;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.gcm.GoogleCloudMessaging;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.media.MediaPlayer;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.app.Activity;
import android.app.ActivityManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager.NameNotFoundException;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
//https://bitbucket.org/jquak1/fyp
import android.widget.TextView.OnEditorActionListener;

/**
 * This class will display sensors information retrieved from the phone's sensor
 * Current sensors implemented: proximity, accelerometer, ambience light, ambience temperature
 * Other info displayed: Phone model, current date & time
 * @author June
 *
 */
public class MainActivity extends Activity implements SensorEventListener {
	public static DbHelper db;
	
	/* Declarations of UI */
	private TextView manuTv, modelTv, timeTv, proximityTv, accelerometerTv1, accelerometerTv2, accelerometerTv3, lightTv, locTv;
	private TextView TextView02, linearAccTv1, linearAccTv2, linearAccTv3, dateTv, magTv1, magTv2, magTv3;
	private TextView driftX, driftY, driftZ, ipAddr, timeInterval;
	private TextView barometerTv;
	private Handler proximityTvHandler, accelerometerTvHandler, linearaccelerometerTvHandler, lightHandler, amTempHandler, barometerHandler;
	private Handler locHandler, gyroHandler, magHandler;
	private Handler delayHandler;
	private SensorManager mSensorManager;
	private Button btnStart, displayData, btnRecordAndTest;
	private Sensor mProximity, mAccelerometer, mLight, mGyro, mMag, mGyroNew, mLinearAcc, mBarometer;

	/* Declarations of global variables for sensors values */
	float[] accVals = new float[3];
	float[] magVals = new float[3];
	float[] gyroVals = new float[3];
	float[] linearAccVals = new float[3];
	float[] barometerVal = new float[1];

	final float[] mValuesMagnet = new float[3];
	final float[] mValuesAccel = new float[3];
	final float[] mValuesOrientation = new float[3];
	final float[] mRotationMatrix = new float[9];
	final float[] mValueBarometer = new float[1];

	String sAccX, sAccY, sAccZ, sgyroX, sgyroY, sgyroZ, sMagX, sMagY, sMagZ, sLinearX, sLinearY, sLinearZ;

	final float ALPHA = (float) 0.15;	

//	/* Declarations for HMM */
//	TreeMap<String, Hmm<ObservationVector>> hmms;
//	private ArrayList<ObservationVector> ov;
//	String[] modelnames = new String[]{"model_Lying on bed.txt","model_Running.txt", "model_Sitting.txt", "model_Standing.txt", "model_Walking.txt"};

	/* Declarations for GCM */
	private String TAG = "hiiamthemainactivity";
	private final static int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
	private String SENDER_ID = "1084992707088";
	public static String lastActivity= "";

	private HTTPHandler httpHandler, gcmRegisterHandler;
	private ClientToServerContainer ctsc;
	
	/*Textbox for IP Addr*/
	public static String ipAddrValue= "";
	public static String timeIntervalValue= "";
	
	public static int activityCode=0;

	GoogleCloudMessaging gcm;
	AtomicInteger msgId = new AtomicInteger();
	SharedPreferences prefs;
	String regid;

	/* Declarations of global variables to be used later */
	public static MainActivity ma;

	private boolean recording = false , testing = false;
	private Date recordingStartTime, recordingEndTime;
	
	SharedPreferences sharedpreferences;
	public static final String MyPREFERENCES = "MyPrefs" ;
	public static final String IPAddr = "ipKey"; 
	SharedPreferences sharedpreferences1;
	public static final String MyPREFERENCES1 = "MyPrefs1" ;
	public static final String TimeInterval = "timeInterval";
	public static int periodRecord = 0;
	

	/* Called upon user's starting the application {initialize the program} */
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		db = new DbHelper(getApplicationContext());
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		initialize();

		/* Setting variables to the GUI in JunesTrackingSystem > res > layout > activity_main.xml */
		modelTv = (TextView)findViewById(R.id.model_tv);
		manuTv = (TextView)findViewById(R.id.manu_tv);
		timeTv = (TextView)findViewById(R.id.time_tv);
		proximityTv = (TextView)findViewById(R.id.proximity_tv);
		lightTv = (TextView)findViewById(R.id.light_tv);
		barometerTv= (TextView)findViewById(R.id.barometer_tv);
		locTv = (TextView)findViewById(R.id.loc_tv);
		TextView02 = (TextView)findViewById(R.id.TextView02);
		btnStart = (Button)findViewById(R.id.btnStart);
		displayData = (Button)findViewById(R.id.displayData);
		btnRecordAndTest = (Button)findViewById(R.id.btnRecordAndTest);
		magTv1 = (TextView)findViewById(R.id.mag_tv1);
		magTv2 = (TextView)findViewById(R.id.mag_tv2);
		magTv3 = (TextView)findViewById(R.id.mag_tv3);
		accelerometerTv1 = (TextView)findViewById(R.id.accelerometer_tv1);
		accelerometerTv2 = (TextView)findViewById(R.id.accelerometer_tv2);
		accelerometerTv3 = (TextView)findViewById(R.id.accelerometer_tv3);
		linearAccTv1 = (TextView)findViewById(R.id.linearAccTv1);
		linearAccTv2 = (TextView)findViewById(R.id.linearAccTv2);
		linearAccTv3 = (TextView)findViewById(R.id.linearAccTv3);
		driftX = (TextView)findViewById(R.id.driftX); 
		driftY = (TextView)findViewById(R.id.driftY); 
		driftZ = (TextView)findViewById(R.id.driftZ);
		ipAddr = (EditText)findViewById(R.id.txtIpAddr);
		timeInterval = (EditText)findViewById(R.id.txtTimeInterval);

		proximityTvHandler = new Handler();
		accelerometerTvHandler = new Handler();
		lightHandler = new Handler();
		barometerHandler = new Handler();
		amTempHandler = new Handler();
		locHandler = new Handler();
		gyroHandler = new Handler();
		magHandler = new Handler();
		httpHandler= new HTTPHandler();
		gcmRegisterHandler = new HTTPHandler();
		delayHandler = new Handler();
		linearaccelerometerTvHandler = new Handler();
		
		
		ActivityManager activityManager = (ActivityManager) getSystemService(ACTIVITY_SERVICE);
		
		Toast.makeText(getApplicationContext(), "Available Memory: " + Integer.toString(activityManager.getMemoryClass()) , Toast.LENGTH_SHORT).show();
		
		sharedpreferences = getSharedPreferences(MyPREFERENCES, Context.MODE_PRIVATE);
		if (sharedpreferences.contains(IPAddr))
	      {
	         ipAddr.setText(sharedpreferences.getString(IPAddr, ""));

	      }
		
		sharedpreferences1 = getSharedPreferences(MyPREFERENCES1, Context.MODE_PRIVATE);
		if (sharedpreferences1.contains(TimeInterval))
	      {
	         timeInterval.setText(sharedpreferences1.getString(TimeInterval, ""));

	      }
		
		// Check device to see if Google Play is installed because GCM requires google play
		if (checkPlayServices()) {
			gcm = GoogleCloudMessaging.getInstance(this);
			//unique identifier for phone (saved in DB). when DB send GCM to phone, it'll send to this ID
			//when regid is empty, it'll register in the background
			//regid == unique to phone, user, app
			regid = getRegistrationId(getApplicationContext());

			if (regid.isEmpty()) {
				registerInBackground();
			}
		}
		
		//not needed, maybe?
		gcmRegisterHandler.setOnResponseReceivedListener(new OnResponseReceivedListener() {

			@Override
			public void onResponseReceived(String receivedString, boolean success) {
				Toast.makeText(getApplicationContext(), "Received   " + receivedString , Toast.LENGTH_SHORT).show();
				Log.i(TAG,"successfully receive1");
			}
		});
		
		//app talk to server (response back to app)
		httpHandler.setOnResponseReceivedListener(new OnResponseReceivedListener() {

			@Override
			public void onResponseReceived(String receivedString, boolean success) {
				Intent sharingIntent = new Intent(Intent.ACTION_SEND);
				sharingIntent.setType("text/plain");
				sharingIntent.putExtra(android.content.Intent.EXTRA_TEXT, receivedString);
				sharingIntent.putExtra(android.content.Intent.EXTRA_SUBJECT, "Error Msg");
				//startActivity(Intent.createChooser(sharingIntent, "Share using"));
				Toast.makeText(getApplicationContext(), "Received   " + receivedString , Toast.LENGTH_SHORT).show();
				Log.i(TAG,"successfully receive2");

			}
		});

		//all listeners must be created each time app is created, else click nth happen
		onClickEvents();
		
		//Set IP addr to String when entered
		
		if (!ipAddr.getEditableText().toString().equals("")){
			ipAddrValue = ipAddr.getEditableText().toString();
		}
		detectDone();
		
		if (!timeInterval.getEditableText().toString().equals("")){
			timeIntervalValue = timeInterval.getEditableText().toString();
		}
		detectDone1();
		
		/* Set up different threads */
		Thread timeThread = null;
		Runnable timeRunnableThread = new CountDownRunner();
		timeThread = new Thread(timeRunnableThread);   
		timeThread.start(); 

		Thread collectTestDataThread = null;
		Runnable testDataRunnableThread = new CountDownRunnerForEvery2SecTestData();
		collectTestDataThread = new Thread(testDataRunnableThread);   
		collectTestDataThread.start(); 
		
		// Get an instance of the sensor service, and use that to get an instance of a particular sensor.
		mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
		mProximity = mSensorManager.getDefaultSensor(Sensor.TYPE_PROXIMITY);
		mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
		mLight = mSensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
		mBarometer = mSensorManager.getDefaultSensor(Sensor.TYPE_PRESSURE);
		mMag = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
		mGyro = mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
		mLinearAcc = mSensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
		
		ma = this;
		
//		modelTv.setText(" " + android.os.Build.MODEL);
//		manuTv.setText(" " + android.os.Build.MANUFACTURER);

//		/**
//		 * To track the location via GPS, but battery drain too much, so remove it first
//		 */
//		LocationManager locationManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);
//
//		// Define a listener that responds to location updates
//		LocationListener locationListener = new LocationListener() {
//			public void onStatusChanged(String provider, int status, Bundle extras) {}
//			public void onProviderEnabled(String provider) {}
//			public void onProviderDisabled(String provider) {}
//
//			@Override
//			public void onLocationChanged(Location location) {
//				String acc = Float.toString(location.getAccuracy());
//				double lat = location.getLatitude();
//				double longitude = location.getLongitude();
//				//makeUseOfNewLocation(location);
//				locTv.setText("Accuracy: " + acc + " \nLatitude: " + lat + " \nLongitude: " + longitude);
//
//
//			}
//		};
		//Register the listener with the Location Manager to receive location updates
//		locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListener);


		//To retrieve out db4o objects
		//		ArrayList<ActivityTest>  arrAt =  new ArrayList<ActivityTest>(Db4oHelper.getInstance(getApplicationContext()).db().query(ActivityTest.class));
		//		String atString ="";
		//		for(ActivityTest at:arrAt){
		//			atString += at.getActivity() + " - " + at.getDateNow().toString()+"\n";
		//		}
		//		Toast.makeText(getApplicationContext(), atString, Toast.LENGTH_SHORT).show();
		//	

	}
	
	private void initialize() {
	        getBaseContext().getApplicationContext().sendBroadcast(
	                new Intent("StartupReceiver_Manual_Start"));
	}//MICH HERE
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	
	class CountDownRunner implements Runnable{
		public void run() {
			while(!Thread.currentThread().isInterrupted()){
				try {
					displayTimeAndDate();
					Thread.sleep(1000); // Pause of 1 Second
				} catch (InterruptedException e) {
					Thread.currentThread().interrupt();
				}catch(Exception e){
				}
			}
		}
	}
	
	/* To display real time date & time */
	public void displayTimeAndDate() {
		runOnUiThread(new Runnable() {
			public void run() {
				try{
					timeTv = (TextView)findViewById(R.id.time_tv);
					dateTv = (TextView)findViewById(R.id.date_tv);
					SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy");
					SimpleDateFormat sdf1 = new SimpleDateFormat("HH:mm:ss");
					String currentDate = sdf.format(new Date());
					String currentTime = sdf1.format(new Date());
					String curDate = " " + currentDate;
					String curTime = " " + currentTime;
					timeTv.setText(curTime);
					dateTv.setText(curDate);
				}catch (Exception e) {}
			}
		});
	}
	
	//For collecting test data to be sent to server
	class CountDownRunnerForEvery2SecTestData implements Runnable{
		public void run() {
			while(!Thread.currentThread().isInterrupted()){
				try {
					long timeInterval1 = Long.parseLong(timeIntervalValue)*1000;
					Thread.sleep(timeInterval1); // Pause of 2 Second
					collectTestData();
				} catch (InterruptedException e) {
					Thread.currentThread().interrupt();
				}catch(Exception e){
				}
			}
		}
	}

	public void collectTestData() {
		runOnUiThread(new Runnable() {
			public void run() {
				try{
					if(testing){
						//End time for every 2 seconds
						recordingEndTime = new Date();
						sendToServerTest();
						//Starts a new 2 seconds collection
						recordingStartTime = new Date();
						Db4oHelper.getInstance(getApplicationContext()).db().store(new GyroscopeDetails(Float.parseFloat(driftX.getText().toString()),Float.parseFloat(driftY.getText().toString()),Float.parseFloat(driftZ.getText().toString()),recordingStartTime));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new MagneticFieldDetails(Float.parseFloat(magTv1.getText().toString()),Float.parseFloat(magTv2.getText().toString()),Float.parseFloat(magTv3.getText().toString()),recordingStartTime));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new AccelerometerDetails(Float.parseFloat(accelerometerTv1.getText().toString()),Float.parseFloat(accelerometerTv2.getText().toString()),Float.parseFloat(accelerometerTv3.getText().toString()),recordingStartTime));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new LinearAccDetails(Float.parseFloat(linearAccTv1.getText().toString()),Float.parseFloat(linearAccTv2.getText().toString()),Float.parseFloat(linearAccTv3.getText().toString()),recordingStartTime));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new BarometerDetails(Float.parseFloat(barometerTv.getText().toString()), recordingStartTime)); //mich: not sure needed or not, why light no have?
						db.createGyro(new GyroscopeDetails(Float.parseFloat(driftX.getText().toString()),Float.parseFloat(driftY.getText().toString()),Float.parseFloat(driftZ.getText().toString()),recordingStartTime, activityCode));
						db.createMag(new MagneticFieldDetails(Float.parseFloat(magTv1.getText().toString()),Float.parseFloat(magTv2.getText().toString()),Float.parseFloat(magTv3.getText().toString()),recordingStartTime, activityCode));
						db.createAcc(new AccelerometerDetails(Float.parseFloat(accelerometerTv1.getText().toString()),Float.parseFloat(accelerometerTv2.getText().toString()),Float.parseFloat(accelerometerTv3.getText().toString()),recordingStartTime, activityCode));
						db.createLinearAcc(new LinearAccDetails(Float.parseFloat(linearAccTv1.getText().toString()),Float.parseFloat(linearAccTv2.getText().toString()),Float.parseFloat(linearAccTv3.getText().toString()),recordingStartTime, activityCode));
						db.createBaro(new BarometerDetails(Float.parseFloat(barometerTv.getText().toString()), recordingStartTime, activityCode)); 
					}
				}catch (Exception e) {}
			}
		});
	}

	//	class GetSensorReadingEveryTenMs implements Runnable{
	//		// @Override
	//		public void run() {
	//			while(!Thread.currentThread().isInterrupted()){
	//				try {
	//					getReading();
	//					Thread.sleep(10); // Pause of 1 Second
	//				} catch (InterruptedException e) {
	//					Thread.currentThread().interrupt();
	//				}catch(Exception e){
	//				}
	//			}
	//		}
	//	}

	//	public void getReading() {
	//		runOnUiThread(new Runnable() {
	//			public void run() {
	//				try{
	//					if(ov!=null){
	//						ov.add(new ObservationVector(new double[]{Double.parseDouble(accelerometerTv1.getText().toString()), Double.parseDouble(accelerometerTv2.getText().toString()), Double.parseDouble(accelerometerTv3.getText().toString())}));
	//						if(ov.size()>100){
	//							String largestValue = "";
	//							double value = -1.7976931348623157E308;
	//							//test against each of the 5 hmms
	//							for(Map.Entry<String, Hmm<ObservationVector>> hmm : hmms.entrySet()){
	//								//Map.Entry<String, Hmm<ObservationVector>> hmmPairs = (Map.Entry<String, Hmm<ObservationVector>>)hmmIterator.next();
	//								System.out.print(hmm.getKey() + "\t: ");
	//								ViterbiCalculator vc = new ViterbiCalculator(ov, hmm.getValue());
	//								System.out.println(vc.lnProbability());
	//								if(vc.lnProbability()>value){
	//									value = vc.lnProbability();
	//									largestValue = hmm.getKey();
	//								}
	//								actTv.setText(largestValue);
	//								//hmmIterator.remove();
	//							}
	//							ov.clear();
	//						}
	//					}
	//				}catch (Exception e) {}
	//			}
	//		});
	//	}
	
	public void copyDBtoSD() throws IOException{
		Log.i("tag", "start copying");
		InputStream myInput = new FileInputStream("/data/data/com.fyp.june.trackingsystem/databases/ADL.db");
		Log.i("tag", "input stream ok");
		File directory = new File("/storage/extSdCard/Android/data/FYP");
		if (!directory.exists()) {
		    directory.mkdirs();
		}
		Log.i("tag", "can find file dir ok");
		OutputStream myOutput = new FileOutputStream(directory.getPath() + "/ADL.db");
		Log.i("tag", "output stream ok");
		byte[] buffer = new byte[1024];
		int length;
		while ((length = myInput.read(buffer)) > 0) {
		    myOutput.write(buffer, 0, length);
		}
		Log.i("mich~~~~~~~~", "copied to storage");
		myOutput.flush();
		myOutput.close();
		myInput.close();
	}
	
	@Override
	public void onAccuracyChanged(Sensor arg0, int arg1) {
	}

	/**
	 * Application to display sensors information whenever sensor event changed
	 * Sensors: Proximity, accelerometer, ambient temp, ambient light
	 */
	@Override
	public void onSensorChanged(SensorEvent event) {
		//To stop recording after 10seconds and send collected data to server
		if(recording && new Date().getTime()-recordingStartTime.getTime() > periodRecord){ //MICH to edit 10 seconds here
			recording = false;
			recordingEndTime = new Date();
			btnStart.setText("Start Recording");
			Toast.makeText(getApplicationContext(), "Recording stopped", Toast.LENGTH_SHORT).show();

			//			Intent i = new Intent(getApplicationContext(), PopupAlert.class);
			//    		i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
			//    		getApplicationContext().startActivity(i);

			//sendToServer();
			MediaPlayer mp = MediaPlayer.create(MainActivity.this, R.raw.start_sound); //MICH sound here
			mp.start();
			
			db.closeDB();
			Db4oHelper.getInstance(getApplicationContext()).db().close();
		}
		
		//low filtered accelerometer
		//http://blog.thomnichols.org/2011/08/smoothing-sensor-data-with-a-low-pass-filter
		if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER){
			accVals = lowPass( event.values.clone(), accVals );
			sAccX = String.format("%.3f", accVals[0]);
			sAccY = String.format("%.3f", accVals[1]);
			sAccZ = String.format("%.3f", accVals[2]);

			accelerometerTvHandler.post(new Runnable() {
				@Override
				public void run() {
					accelerometerTv1.setText(sAccX);
					accelerometerTv2.setText(sAccY);
					accelerometerTv3.setText(sAccZ);
					
					//If data collection for test and train has not ended, will store records into db4o objects each time sensor changes
					if(testing || (recording && new Date().getTime()-recordingStartTime.getTime() < periodRecord)){
						Log.i("michelle~~~~~~~~~~~~","add acc~~~~~~~~~~~~~~~~~~");
						db.createAcc(new AccelerometerDetails(Float.parseFloat(accelerometerTv1.getText().toString()),Float.parseFloat(accelerometerTv2.getText().toString()),Float.parseFloat(accelerometerTv3.getText().toString()),new Date(), activityCode));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new AccelerometerDetails(Float.parseFloat(accelerometerTv1.getText().toString()),Float.parseFloat(accelerometerTv2.getText().toString()),Float.parseFloat(accelerometerTv3.getText().toString()),new Date()));
					}		

				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_LINEAR_ACCELERATION){
			linearAccVals = event.values.clone();
			sLinearX = String.format("%.3f", linearAccVals[0]);
			sLinearY = String.format("%.3f", linearAccVals[1]);
			sLinearZ = String.format("%.3f", linearAccVals[2]);
			linearaccelerometerTvHandler.post(new Runnable() {
				@Override
					public void run() {
					linearAccTv1.setText(sLinearX);
					linearAccTv2.setText(sLinearY);
					linearAccTv3.setText(sLinearZ);
					
					//If data collection for test and train has not ended, will store records into db4o objects each time sensor changes
					if(testing || (recording && new Date().getTime()-recordingStartTime.getTime() < periodRecord)){
						db.createLinearAcc(new LinearAccDetails(Float.parseFloat(linearAccTv1.getText().toString()),Float.parseFloat(linearAccTv2.getText().toString()),Float.parseFloat(linearAccTv3.getText().toString()),new Date(), activityCode));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new LinearAccDetails(Float.parseFloat(linearAccTv1.getText().toString()),Float.parseFloat(linearAccTv2.getText().toString()),Float.parseFloat(linearAccTv3.getText().toString()),new Date()));
					}	
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_GYROSCOPE){

			SensorManager.getRotationMatrix(mRotationMatrix, null, mValuesAccel, mValuesMagnet);
			SensorManager.getOrientation(mRotationMatrix, mValuesOrientation);
			
			gyroVals = event.values.clone();
			sgyroX = String.format("%.3f", gyroVals[0]);
			sgyroY = String.format("%.3f", gyroVals[1]);
			sgyroZ = String.format("%.3f", gyroVals[2]);
			gyroHandler.post(new Runnable() {
				@Override
				public void run() {
					driftX.setText(sgyroX);
					driftY.setText(sgyroY);
					driftZ.setText(sgyroZ);
					
					//If data collection for test and train has not ended, will store records into db4o objects each time sensor changes
					if(testing || (recording && new Date().getTime()-recordingStartTime.getTime() < periodRecord)){
						db.createGyro(new GyroscopeDetails(Float.parseFloat(driftX.getText().toString()),Float.parseFloat(driftY.getText().toString()),Float.parseFloat(driftZ.getText().toString()),new Date(), activityCode));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new GyroscopeDetails(Float.parseFloat(driftX.getText().toString()),Float.parseFloat(driftY.getText().toString()),Float.parseFloat(driftZ.getText().toString()),new Date()));
					}
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_MAGNETIC_FIELD){
			magVals = event.values.clone();
			sMagX = String.format("%.3f", magVals[0]);
			sMagY = String.format("%.3f", magVals[1]);
			sMagZ = String.format("%.3f", magVals[2]);
			System.arraycopy(event.values, 0, mValuesMagnet, 0, 3);

			magHandler.post(new Runnable() {
				@Override
				public void run() {
					magTv1.setText(sMagX);
					magTv2.setText(sMagY);
					magTv3.setText(sMagZ);
					
					//If data collection for test and train has not ended, will store records into db4o objects each time sensor changes
					if(testing || (recording && new Date().getTime()-recordingStartTime.getTime() < periodRecord)){
						db.createMag(new MagneticFieldDetails(Float.parseFloat(magTv1.getText().toString()),Float.parseFloat(magTv2.getText().toString()),Float.parseFloat(magTv3.getText().toString()),new Date(), activityCode));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new MagneticFieldDetails(Float.parseFloat(magTv1.getText().toString()),Float.parseFloat(magTv2.getText().toString()),Float.parseFloat(magTv3.getText().toString()),new Date()));
					}
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_PROXIMITY){
			final String distance = Float.toString(event.values[0]);
			proximityTvHandler.post(new Runnable() {
				@Override
				public void run() {
					proximityTv.setText(" " + distance);
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_PRESSURE){
			barometerVal = event.values.clone();
			float pressure = event.values[0];
			final String sPressure = String.format("%.3f", pressure);
			barometerHandler.post(new Runnable() {
				@Override
				public void run() {
					barometerTv.setText(" " + sPressure);
					
					if (testing||(recording && new Date().getTime()-recordingStartTime.getTime() <periodRecord)){
						db.createBaro(new BarometerDetails(Float.parseFloat(barometerTv.getText().toString()), new Date(), activityCode));
						Db4oHelper.getInstance(getApplicationContext()).db().store(new BarometerDetails(Float.parseFloat(barometerTv.getText().toString()), new Date()));
			
					}
				}
			});
		}
		
		else if(event.sensor.getType()==Sensor.TYPE_LIGHT){
			float light = event.values[0];
			final String sLight = String.format("%.3f", light);

			lightHandler.post(new Runnable() {
				@Override
				public void run() {
					lightTv.setText(" " + sLight);
					
					//If data collection for test and train has not ended, will store records into db4o objects each time sensor changes
//					if(testing || (recording && new Date().getTime()-recordingStartTime.getTime() < 10000)){
//						Db4oHelper.getInstance(getApplicationContext()).db().store(new AmbientLightDetails(Float.parseFloat(lightTv.getText().toString()),Float.parseFloat(amTempTv.getText().toString()),new Date()));
//					}
				}
			});
		}
	}
	
    private void startRecording(int activityType){
    	MediaPlayer mp = MediaPlayer.create(this, R.raw.stoprecording); 
    	mp.start();
    	try{
    		MainActivity.ma.delayBeforeRecording(activityType);
    	}catch(Exception e){
    		e.printStackTrace();
    	}
    }

	public void delayBeforeRecording(int activityType){
		//lastActivity = activityType;
		/*if (activityType.equals("Standing")) activityCode=1;
		if (activityType.equals("Sitting")) activityCode=2;
		if (activityType.equals("Walking")) activityCode=3;
		if (activityType.equals("Running")) activityCode=4;
		if (activityType.equals("Lying on bed")) activityCode=5;*/
		activityCode=activityType;
		System.out.println(periodRecord);
		delayHandler.postDelayed(new Runnable() {

			@Override
			public void run() {
				MediaPlayer mp = MediaPlayer.create(MainActivity.this, R.raw.stoprecording); 
				mp.start();
				Toast.makeText(getApplicationContext(), "Recording started", Toast.LENGTH_SHORT).show();
				recording = true;
				recordingStartTime = new Date();
				Log.i("michelle~~~~~~~~~~~~","delay before recording~~~~~~~~~~~~~~~~~~");
				Db4oHelper.getInstance(getApplicationContext()).db().store(new GyroscopeDetails(Float.parseFloat(driftX.getText().toString()),Float.parseFloat(driftY.getText().toString()),Float.parseFloat(driftZ.getText().toString()),recordingStartTime));
				Db4oHelper.getInstance(getApplicationContext()).db().store(new MagneticFieldDetails(Float.parseFloat(magTv1.getText().toString()),Float.parseFloat(magTv2.getText().toString()),Float.parseFloat(magTv3.getText().toString()),recordingStartTime));
				Db4oHelper.getInstance(getApplicationContext()).db().store(new AccelerometerDetails(Float.parseFloat(accelerometerTv1.getText().toString()),Float.parseFloat(accelerometerTv2.getText().toString()),Float.parseFloat(accelerometerTv3.getText().toString()),recordingStartTime));
				Db4oHelper.getInstance(getApplicationContext()).db().store(new LinearAccDetails(Float.parseFloat(linearAccTv1.getText().toString()),Float.parseFloat(linearAccTv2.getText().toString()),Float.parseFloat(linearAccTv3.getText().toString()),recordingStartTime));
				Db4oHelper.getInstance(getApplicationContext()).db().store(new BarometerDetails(Float.parseFloat(barometerTv.getText().toString()), recordingStartTime)); //mich: not sure needed or not, why light no have?
				db.createGyro(new GyroscopeDetails(Float.parseFloat(driftX.getText().toString()),Float.parseFloat(driftY.getText().toString()),Float.parseFloat(driftZ.getText().toString()),recordingStartTime, activityCode));
				db.createMag(new MagneticFieldDetails(Float.parseFloat(magTv1.getText().toString()),Float.parseFloat(magTv2.getText().toString()),Float.parseFloat(magTv3.getText().toString()),recordingStartTime, activityCode));
				db.createAcc(new AccelerometerDetails(Float.parseFloat(accelerometerTv1.getText().toString()),Float.parseFloat(accelerometerTv2.getText().toString()),Float.parseFloat(accelerometerTv3.getText().toString()),recordingStartTime, activityCode));
				db.createLinearAcc(new LinearAccDetails(Float.parseFloat(linearAccTv1.getText().toString()),Float.parseFloat(linearAccTv2.getText().toString()),Float.parseFloat(linearAccTv3.getText().toString()),recordingStartTime, activityCode));
				db.createBaro(new BarometerDetails(Float.parseFloat(barometerTv.getText().toString()), recordingStartTime, activityCode)); 
			}
		}, 5000);
	}

	public void onClickEvents(){
		btnStart.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				delayHandler.postDelayed(new Runnable() {

					@Override
					public void run() {
						//Toast.makeText(getApplicationContext(), "Recording started", Toast.LENGTH_SHORT).show();
						//recording = true;
						//recordingStartTime = new Date();
						periodRecord=Integer.parseInt(ipAddr.getEditableText().toString());
						Log.i("period",String.valueOf(periodRecord));
						startRecording(Integer.parseInt(timeInterval.getEditableText().toString()));
						btnStart.setText("Stop Recording");
					}
				}, 5000);	
			}
		});


		btnRecordAndTest.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				//Empty db first then store
				for(AccelerometerDetails ad:new ArrayList<AccelerometerDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(AccelerometerDetails.class)))Db4oHelper.getInstance(getApplicationContext()).db().delete(ad);
				for(GyroscopeDetails gd:new ArrayList<GyroscopeDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(GyroscopeDetails.class)))Db4oHelper.getInstance(getApplicationContext()).db().delete(gd);
				for(MagneticFieldDetails md:new ArrayList<MagneticFieldDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(MagneticFieldDetails.class)))Db4oHelper.getInstance(getApplicationContext()).db().delete(md);
				for(LinearAccDetails ld:new ArrayList<LinearAccDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(LinearAccDetails.class)))Db4oHelper.getInstance(getApplicationContext()).db().delete(ld);
				for (BarometerDetails bb:new ArrayList<BarometerDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(BarometerDetails.class)))Db4oHelper.getInstance(getApplicationContext()).db().delete(bb);
				Db4oHelper.getInstance(getApplicationContext()).db().close();
				//T to F, F to T
				testing = !testing;
				btnRecordAndTest.setText("Start Recording");
				if(testing){
					btnRecordAndTest.setText("Stop Recording");
					recordingStartTime = new Date();
					//Get the first reading for all sensors at same time
					Db4oHelper.getInstance(getApplicationContext()).db().store(new GyroscopeDetails(Float.parseFloat(driftX.getText().toString()),Float.parseFloat(driftY.getText().toString()),Float.parseFloat(driftZ.getText().toString()),recordingStartTime));
					Db4oHelper.getInstance(getApplicationContext()).db().store(new MagneticFieldDetails(Float.parseFloat(magTv1.getText().toString()),Float.parseFloat(magTv2.getText().toString()),Float.parseFloat(magTv3.getText().toString()),recordingStartTime));
					Db4oHelper.getInstance(getApplicationContext()).db().store(new AccelerometerDetails(Float.parseFloat(accelerometerTv1.getText().toString()),Float.parseFloat(accelerometerTv2.getText().toString()),Float.parseFloat(accelerometerTv3.getText().toString()),recordingStartTime));
					Db4oHelper.getInstance(getApplicationContext()).db().store(new LinearAccDetails(Float.parseFloat(linearAccTv1.getText().toString()),Float.parseFloat(linearAccTv2.getText().toString()),Float.parseFloat(linearAccTv3.getText().toString()),recordingStartTime));
					Db4oHelper.getInstance(getApplicationContext()).db().store(new BarometerDetails(Float.parseFloat(barometerTv.getText().toString()), recordingStartTime));
				}
				//				if(ov==null){
				//					hmms = new TreeMap<String, Hmm<ObservationVector>>();
				//					//Db4oHelper.getInstance(getApplicationContext()).db().query(
				//					Log.e("pls work", Environment.getExternalStorageDirectory() + "/hmm.db4o");
				//					File file = new File(Environment.getExternalStorageDirectory() + "/hmm.db4o"); 
				//					if(file.exists()){   
				//						Log.e("it work", Environment.getExternalStorageDirectory() + "/hmm.db4o");
				//					}
				//					//Db4oHelperHMM.getInstance().db();
				//					List<Hmm> hmmlist =  Db4oHelperHMM.getInstance().db().query(Hmm.class);
				//					int m =0;
				//					Log.e("why still no work", Integer.toString(hmmlist.size()));
				//					for(int i=0;i<hmmlist.size();i++){
				//						Log.e("hey", hmmlist.get(i).toString());
				//						//hmms.put(modelnames[m].replace("model_", "").replace(".txt", ""), hmmlist.get(i));
				//						m++;
				//					}
				////					for(Hmm<ObservationVector> oneHmm : hmmlist){
				////						hmms.put(modelnames[m].replace("model_", "").replace(".txt", ""), oneHmm);
				////						m++;
				////					}
				//					Db4oHelperHMM.getInstance().db().close();
				//					ov = new ArrayList<ObservationVector>();
				//				}
			}
		});

		//		displayData.setOnClickListener(new OnClickListener() {
		//			
		//			@Override
		//			public void onClick(View v) {
		//				// TODO Auto-generated method stub
		//				recording=false;
		////				ArrayList<AccelerometerDetails>  arrAD =  new ArrayList<AccelerometerDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(AccelerometerDetails.class));
		////				String adString ="AccX,Y,Z,Date";
		////				for(AccelerometerDetails ad:arrAD){
		////					adString += "\n" + Float.toString(ad.getAccX()) + "," + Float.toString(ad.getAccY()) + "," + Float.toString(ad.getAccZ()) + "," + Long.toString(ad.getDateNow().getTime());
		////					//Db4oHelper.getInstance(getApplicationContext()).db().delete(ad);
		////				}
		//				
		//				//client to server
		//				ctsc = null;
		//				ctsc = new ClientToServerContainer();
		//				ctsc.endTime = recordingEndTime;
		//				ctsc.startTime = recordingStartTime;
		//				ctsc.activityType = lastActivity;
		//				ctsc.uuid = new DeviceUuidFactory(getApplicationContext()).getDeviceUuid().toString();
		//				ctsc.accArraylist = new ArrayList<AccelerometerDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(AccelerometerDetails.class));
		//				ctsc.gyroArraylist = new ArrayList<GyroscopeDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(GyroscopeDetails.class));
		//				ctsc.magArraylist =new ArrayList<MagneticFieldDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(MagneticFieldDetails.class));
		//				GsonFireBuilder builder = new GsonFireBuilder();
		//				builder.dateSerializationPolicy(DateSerializationPolicy.unixTimeMillis);
		//				Gson gson = builder.createGson();//new GsonBuilder().setDateFormat(DateFormat.LONG).create();
		//				List<NameValuePair> nvp = new ArrayList<NameValuePair>();
		//				nvp.add(new BasicNameValuePair("Accelerometer", gson.toJson(ctsc)));
		//				httpHandler.handleHTTP(nvp, "http://ntufyp.jquak.com/services/accelerometer.php");
		//				//ctsc = null;
		//				
		////				ArrayList<GyroscopeDetails>  arrGD =  new ArrayList<GyroscopeDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(GyroscopeDetails.class));
		////				String gdString ="GyroX,Y,Z,Date";
		////				for(GyroscopeDetails gd:arrGD){
		////					gdString += "\n" + Float.toString(gd.getGyroX()) + "," + Float.toString(gd.getGyroY()) + "," + Float.toString(gd.getGyroZ()) + "," + Long.toString(gd.getDateNow().getTime());
		////					//Db4oHelper.getInstance(getApplicationContext()).db().delete(gd);
		////				}
		////				ArrayList<AmbientLightDetails>  arrALD =  new ArrayList<AmbientLightDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(AmbientLightDetails.class));
		////				String aldString ="Light,Temp,Date";
		////				for(AmbientLightDetails al:arrALD){
		////					aldString += "\n" + Float.toString(al.getBrightness()) + "," + Float.toString(al.getTemperature())+ "," + Long.toString(al.getDateNow().getTime());
		////					//Db4oHelper.getInstance(getApplicationContext()).db().delete(al);
		////				}
		////				ArrayList<MagneticFieldDetails>  arrMD =  new ArrayList<MagneticFieldDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(MagneticFieldDetails.class));
		////				String mdString ="MagX,Y,Z,Date";
		////				for(MagneticFieldDetails md:arrMD){
		////					mdString += "\n" + Float.toString(md.getMagX()) + "," + Float.toString(md.getMagY()) + "," + Float.toString(md.getMagZ()) + "," + Long.toString(md.getDateNow().getTime());
		////					//Db4oHelper.getInstance(getApplicationContext()).db().delete(md);
		////				}
		////				
		////				//PROXIMITY NOT DONE YET
		////				Intent sharingIntent = new Intent(Intent.ACTION_SEND);
		////
		////				ArrayList<ActivityTest>  arrAt =  new ArrayList<ActivityTest>(Db4oHelper.getInstance(getApplicationContext()).db().query(ActivityTest.class));
		////				String atString ="";
		////				for(ActivityTest at:arrAt){
		////					atString = at.getActivity();
		////				}
		////				sharingIntent.setType("text/plain");
		////				sharingIntent.putExtra(android.content.Intent.EXTRA_TEXT, adString + "\n\n" +  gdString + "\n\n" + aldString + "\n\n" + mdString);
		////				sharingIntent.putExtra(android.content.Intent.EXTRA_SUBJECT, "Sensors Data for " + atString);
		////				//email contents
		////				startActivity(Intent.createChooser(sharingIntent, "Share using"));
		////				Toast.makeText(getApplicationContext(), adString, Toast.LENGTH_SHORT).show();
		//				//for(ActivityTest at:arrAt)Db4oHelper.getInstance(getApplicationContext()).db().delete(at);
		//				for(AccelerometerDetails ad:(ArrayList<AccelerometerDetails>)ctsc.accArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(ad);
		//				for(GyroscopeDetails gd:(ArrayList<GyroscopeDetails>)ctsc.gyroArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(gd);
		//				//for(AmbientLightDetails al:arrALD)Db4oHelper.getInstance(getApplicationContext()).db().delete(al);
		//				for(MagneticFieldDetails md:(ArrayList<MagneticFieldDetails>)ctsc.magArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(md);
		//				Db4oHelper.getInstance(getApplicationContext()).db().close();
		//				ctsc = null;
		//			}
		//		});
	}

	//open app after it minimizes
	@Override
	protected void onResume() {
		// Register a listener for the sensor.
		super.onResume();
		//		mSensorManager.registerListener(this, mProximity, SensorManager.SENSOR_DELAY_NORMAL);
		//		mSensorManager.registerListener(this, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
		//		mSensorManager.registerListener(this, mAmTemp, SensorManager.SENSOR_DELAY_NORMAL);
		//		mSensorManager.registerListener(this, mMag, SensorManager.SENSOR_DELAY_NORMAL);
		//		mSensorManager.registerListener(this, mLight, SensorManager.SENSOR_DELAY_NORMAL);
		//		mSensorManager.registerListener(this, mGyro, SensorManager.SENSOR_DELAY_NORMAL);
		//		mSensorManager.registerListener(this, mLinearAcc, SensorManager.SENSOR_DELAY_NORMAL);
		//		mSensorManager.registerListener(this, mRotationalVector, SensorManager.SENSOR_DELAY_NORMAL);
		mSensorManager.registerListener(this, mProximity, 50000);
		mSensorManager.registerListener(this, mAccelerometer, 50000);
		//mSensorManager.registerListener(this, mAmTemp, 50000);
		mSensorManager.registerListener(this, mMag, 50000);
		mSensorManager.registerListener(this, mLight, 50000);
		mSensorManager.registerListener(this, mBarometer,50000);
		mSensorManager.registerListener(this, mGyro, 50000);
		mSensorManager.registerListener(this, mLinearAcc, 50000);
		checkPlayServices();
	}//http://stackoverflow.com/questions/9935896/android-accelerometer-registerlistener

	public void setListeners(SensorManager sensorManager, SensorEventListener mEventListener)
	{
		sensorManager.registerListener(mEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), 
				SensorManager.SENSOR_DELAY_FASTEST);
		sensorManager.registerListener(mEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD), 
				SensorManager.SENSOR_DELAY_FASTEST);
		sensorManager.registerListener(mEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE), 
				SensorManager.SENSOR_DELAY_FASTEST);
		sensorManager.registerListener(mEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION), 
				SensorManager.SENSOR_DELAY_FASTEST);
		sensorManager.registerListener(mEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_PRESSURE), 
				SensorManager.SENSOR_DELAY_FASTEST);

	}

	//pause app when go to other app
	@Override
	protected void onPause() {
		// Be sure to unregister the sensor when the activity pauses.
		super.onPause();
		mSensorManager.unregisterListener(this);
	}

	/**
	 * @see http://en.wikipedia.org/wiki/Low-pass_filter#Algorithmic_implementation
	 * @see http://developer.android.com/reference/android/hardware/SensorEvent.html#values
	 */
	protected float[] lowPass( float[] input, float[] output ) {
		if ( output == null ) return input;

		for ( int i=0; i<input.length; i++ ) {
			output[i] = output[i] + ALPHA * (input[i] - output[i]);
		}
		return output;
	}
	
	
	 public void detectDone(){
		 ipAddr.setOnEditorActionListener(new OnEditorActionListener() {
			 @Override
			    public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
			        if (actionId == EditorInfo.IME_ACTION_DONE) {
			            // do your stuff here			        	
			        	if (!ipAddr.getEditableText().toString().equals("")){
			        		ipAddrValue= ipAddr.getEditableText().toString();
			        		 Editor editor = sharedpreferences.edit();
			        	     editor.putString(IPAddr, ipAddrValue);
			        	     editor.commit();
			        	     sendRegistrationIdToBackend(MainActivity.this.getRegistrationId(getApplicationContext()));
			        }
			        }
			        return false;
			    }
			});
		
		 
		 }
	 public void detectDone1(){
		 timeInterval.setOnEditorActionListener(new OnEditorActionListener() {
				
				@Override
				public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
					if (actionId == EditorInfo.IME_ACTION_DONE) {
			            // do your stuff here			        	
			        	if (!timeInterval.getEditableText().toString().equals("")){
			        		timeIntervalValue= timeInterval.getEditableText().toString();
			        		 Editor editor1 = sharedpreferences1.edit();
			        	     editor1.putString(TimeInterval, timeIntervalValue);
			        	     editor1.commit();
			        }
			        }
					return false;
				}
			});}

	public void sendToServer(){
		recording=false;

		//client to server
		ctsc = null;
		ctsc = new ClientToServerContainer();
		ctsc.endTime = recordingEndTime;
		ctsc.startTime = recordingStartTime;
		ctsc.activityType = lastActivity;
		ctsc.uuid = new DeviceUuidFactory(getApplicationContext()).getDeviceUuid().toString();
		ctsc.accArraylist = new ArrayList<AccelerometerDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(AccelerometerDetails.class));
		ctsc.gyroArraylist = new ArrayList<GyroscopeDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(GyroscopeDetails.class));
		ctsc.magArraylist =new ArrayList<MagneticFieldDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(MagneticFieldDetails.class));
		ctsc.linearArraylist =new ArrayList<LinearAccDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(LinearAccDetails.class));
		ctsc.barometerArraylist= new ArrayList<BarometerDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(BarometerDetails.class));
		//Google's Json
		GsonFireBuilder builder = new GsonFireBuilder();
		builder.dateSerializationPolicy(DateSerializationPolicy.unixTimeMillis);
		Gson gson = builder.createGson();
		List<NameValuePair> nvp = new ArrayList<NameValuePair>();
		nvp.add(new BasicNameValuePair("Accelerometer", gson.toJson(ctsc)));
		//httpHandler.handleHTTP(nvp, "http://ntufyp.jquak.com/services/accelerometer.php");
		httpHandler.handleHTTP(nvp, "http://" + ipAddrValue +"/fyp/services/trainingdata.php");//link to php
		//172.22.93.178
		//Empty DB
		for(AccelerometerDetails ad:(ArrayList<AccelerometerDetails>)ctsc.accArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(ad);
		for(GyroscopeDetails gd:(ArrayList<GyroscopeDetails>)ctsc.gyroArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(gd);
		for(MagneticFieldDetails md:(ArrayList<MagneticFieldDetails>)ctsc.magArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(md);
		for(LinearAccDetails ld:(ArrayList<LinearAccDetails>)ctsc.linearArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(ld);
		for(BarometerDetails bb:(ArrayList<BarometerDetails>)ctsc.barometerArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(bb);
		Db4oHelper.getInstance(getApplicationContext()).db().close();
		
		ctsc = null;
		MediaPlayer mp = MediaPlayer.create(MainActivity.this, R.raw.start_sound); //MICH sound here
		mp.start();

	}
	//This method sends test data to the server
	public void sendToServerTest(){
		recording=false;

		//client to server
		ctsc = null;
		ctsc = new ClientToServerContainer();
		ctsc.endTime = recordingEndTime;
		ctsc.startTime = recordingStartTime;
		ctsc.activityType = lastActivity;
		ctsc.uuid = new DeviceUuidFactory(getApplicationContext()).getDeviceUuid().toString();
		ctsc.accArraylist = new ArrayList<AccelerometerDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(AccelerometerDetails.class));
		ctsc.gyroArraylist = new ArrayList<GyroscopeDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(GyroscopeDetails.class));
		ctsc.magArraylist =new ArrayList<MagneticFieldDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(MagneticFieldDetails.class));
		ctsc.linearArraylist =new ArrayList<LinearAccDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(LinearAccDetails.class));
		ctsc.barometerArraylist = new ArrayList<BarometerDetails>(Db4oHelper.getInstance(getApplicationContext()).db().query(BarometerDetails.class));
		
		GsonFireBuilder builder = new GsonFireBuilder();
		builder.dateSerializationPolicy(DateSerializationPolicy.unixTimeMillis);
		Gson gson = builder.createGson();
		List<NameValuePair> nvp = new ArrayList<NameValuePair>();
		nvp.add(new BasicNameValuePair("AccelerometerTest", gson.toJson(ctsc)));
		//httpHandler.handleHTTP(nvp, "http://ntufyp.jquak.com/services/accelerometer.php");
		httpHandler.handleHTTP(nvp, "http://" + ipAddrValue +"/fyp/services/testingdata.php");
		//http://172.22.93.178/
		
		Toast.makeText(getApplicationContext(),"sent to server", Toast.LENGTH_SHORT).show();
		
		//Empty DB
		for(AccelerometerDetails ad:(ArrayList<AccelerometerDetails>)ctsc.accArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(ad);
		for(GyroscopeDetails gd:(ArrayList<GyroscopeDetails>)ctsc.gyroArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(gd);
		for(MagneticFieldDetails md:(ArrayList<MagneticFieldDetails>)ctsc.magArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(md);
		for(LinearAccDetails ld:(ArrayList<LinearAccDetails>)ctsc.linearArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(ld);
		for(BarometerDetails bb:(ArrayList<BarometerDetails>)ctsc.barometerArraylist)Db4oHelper.getInstance(getApplicationContext()).db().delete(bb);
		Db4oHelper.getInstance(getApplicationContext()).db().close();
		ctsc = null;
	}
	
	// Check device to see if Google Play is installed because GCM requires google play
	private boolean checkPlayServices() {
		int resultCode = GooglePlayServicesUtil.isGooglePlayServicesAvailable(this);
		if (resultCode != ConnectionResult.SUCCESS) {
			if (GooglePlayServicesUtil.isUserRecoverableError(resultCode)) {
				GooglePlayServicesUtil.getErrorDialog(resultCode, this,
						PLAY_SERVICES_RESOLUTION_REQUEST).show();
			} else {
				Log.i("GCM", "This device is not supported.");
				finish();
			}
			return false;
		}
		return true;
	}
	
	//unique identifier for phone (saved in DB). when DB send GCM to phone, it'll send to this ID
	//when regid is empty, it'll register in the background
	//regid == unique to phone, user, app
	private String getRegistrationId(Context context) {
		final SharedPreferences prefs = getGCMPreferences(context);
		String registrationId = prefs.getString("PROPERTY_REG_ID", "");
		if (registrationId.isEmpty()) {
			Log.i(TAG, "Registration not found.");
			return "";
		}
		// Check if app was updated; if so, it must clear the registration ID
		// since the existing regID is not guaranteed to work with the new
		// app version.
		int registeredVersion = prefs.getInt("PROPERTY_APP_VERSION", Integer.MIN_VALUE);
		int currentVersion = getAppVersion(context);
		if (registeredVersion != currentVersion) {
			Log.i(TAG, "App version changed.");
			return "";
		}
		return registrationId;
	}
	
	private SharedPreferences getGCMPreferences(Context context) {
		// This sample app persists the registration ID in shared preferences, but
		// how you store the regID in your app is up to you.
		return getSharedPreferences(MainActivity.class.getSimpleName(),
				Context.MODE_PRIVATE);
	}
	/**
	 * @return Application's version code from the {@code PackageManager}.
	 */
	private static int getAppVersion(Context context) {
		try {
			PackageInfo packageInfo = context.getPackageManager()
					.getPackageInfo(context.getPackageName(), 0);
			return packageInfo.versionCode;
		} catch (NameNotFoundException e) {
			// should never happen
			throw new RuntimeException("Could not get package name: " + e);
		}
	}
	/**
	 * Registers the application with GCM servers asynchronously.
	 * <p>
	 * Stores the registration ID and app versionCode in the application's
	 * shared preferences.
	 */
	private void registerInBackground() {
		new AsyncTask<Void, Void, Void>() {
			String msg = "";
			@Override
			protected Void doInBackground(Void... params) {

				try {
					if (gcm == null) {
						gcm = GoogleCloudMessaging.getInstance(getApplicationContext());
					}
					regid = gcm.register(SEN DER_ID);
					msg = "Device registered, registration ID=" + regid;

					// You should send the registration ID to your server over HTTP,
					// so it can use GCM/HTTP or CCS to send messages to your app.
					// The request to your server should be authenticated if your app
					// is using accounts.
					sendRegistrationIdToBackend(regid);

					// For this demo: we don't need to send it because the device
					// will send upstream messages to a server that echo back the
					// message using the 'from' address in the message.

					// Persist the regID - no need to register again.
					storeRegistrationId(getApplicationContext(), regid);
				} catch (IOException ex) {
					msg = "Error :" + ex.getMessage();
					// If there is an error, don't just keep trying to register.
					// Require the user to click a button again, or perform
					// exponential back-off.
				}
				return null;
				//return msg;
			}

			@Override
			protected void onPostExecute(Void arg0 ) {
				//mDisplay.append(msg + "\n");
			}
		}.execute(null, null, null);
	}
	
	/**
	 * Sends the registration ID to your server over HTTP, so it can use GCM/HTTP
	 * or CCS to send messages to your app. Not needed for this demo since the
	 * device sends upstream messages to a server that echoes back the message
	 * using the 'from' address in the message.
	 */
	private void sendRegistrationIdToBackend(String regid) {
		List<NameValuePair> nvp = new ArrayList<NameValuePair>();
		nvp.add(new BasicNameValuePair("gcmId", regid));
		nvp.add(new BasicNameValuePair("deviceid", new DeviceUuidFactory(getApplicationContext()).getDeviceUuid().toString()));
		//httpHandler.handleHTTP(nvp, "http://ntufyp.jquak.com/services/gcm.php");
		httpHandler.handleHTTP(nvp, "http://" + ipAddrValue +"/fyp/services/gcm.php");
	}
	/**
	 * Stores the registration ID and app versionCode in the application's
	 * {@code SharedPreferences}.
	 *
	 * @param context application's context.
	 * @param regId registration ID
	 */
	private void storeRegistrationId(Context context, String regId) {
		final SharedPreferences prefs = getGCMPreferences(context);
		int appVersion = getAppVersion(context);
		Log.i(TAG, "Saving regId on app version " + appVersion);
		SharedPreferences.Editor editor = prefs.edit();
		editor.putString("PROPERTY_REG_ID", regId);
		editor.putInt("PROPERTY_APP_VERSION", appVersion);
		editor.commit();
	}

	//Disable back button
	@Override
	public void onBackPressed() {
	}
}

