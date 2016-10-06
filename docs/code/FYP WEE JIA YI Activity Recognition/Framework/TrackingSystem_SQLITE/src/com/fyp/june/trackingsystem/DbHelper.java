package com.fyp.june.trackingsystem;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import com.fyp.june.entities.*;

import android.content.ContentValues;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Environment;
import android.util.Log;

public class DbHelper extends SQLiteOpenHelper {

	// Logcat tag
	private static final String LOG = "DbHelper";

	// Database Version
	private static final int DATABASE_VERSION = 1;

	// Database Name
	private static final String DATABASE_NAME = "ADL.db";

	// Table Names
	private static final String TABLE_Accelerometer = "accelerometer";
	private static final String TABLE_LinearAcc = "linearacc";
	private static final String TABLE_Gyroscope = "gyroscope";
	private static final String TABLE_MagneticField = "magneticfield";
	private static final String TABLE_Barometer = "barometer";

	// Common column names
	private static final String KEY_ID="id";
	private static final String KEY_CREATED_AT = "time"; 
	private static final String KEY_activity = "activity";

	// Accelerometer Table - column names
	private static final String KEY_accX ="accX";
	private static final String KEY_accY ="accY";
	private static final String KEY_accZ ="accZ";

	// Linearacc Table - column names
	private static final String KEY_laccX ="laccX";
	private static final String KEY_laccY ="laccY";
	private static final String KEY_laccZ ="laccZ";

	// Gyroscope Table - column names
	private static final String KEY_gX ="gX";
	private static final String KEY_gY ="gY";
	private static final String KEY_gZ ="gZ";
	
	// MagneticField Table - column names
	private static final String KEY_mX ="mX";
	private static final String KEY_mY ="mY";
	private static final String KEY_mZ ="mZ";
	
	// Barometer Table - column names
	private static final String KEY_baro = "baro";

	// Table Create Statements
	// Acc table create statement
	private static final String CREATE_TABLE_Accelerometer = 
			"CREATE TABLE "
			+TABLE_Accelerometer+" ( " +KEY_ID+ " INTEGER PRIMARY KEY," 
			+ KEY_accX + " FLOAT," 
			+ KEY_accY + " FLOAT,"
			+ KEY_accZ + " FLOAT,"
			+ KEY_activity + " INTEGER," 
			+ KEY_CREATED_AT + " INTEGER" + ")";

	// LinearAcc table create statement
	private static final String CREATE_TABLE_LinearAcc = "CREATE TABLE "
			+ TABLE_LinearAcc + "(" + KEY_ID + " INTEGER PRIMARY KEY," 
			+ KEY_laccX + " FLOAT," 
			+ KEY_laccY + " FLOAT,"
			+ KEY_laccZ + " FLOAT,"
			+ KEY_activity + " INTEGER," 
			+ KEY_CREATED_AT + " INTEGER" + ")";

	// gyroscope table create statement
	private static final String CREATE_TABLE_Gyroscope= "CREATE TABLE "
			+ TABLE_Gyroscope + "(" + KEY_ID + " INTEGER PRIMARY KEY," 
			+ KEY_gX + " FLOAT," 
			+ KEY_gY + " FLOAT,"
			+ KEY_gZ + " FLOAT,"
			+ KEY_activity + " INTEGER," 
			+ KEY_CREATED_AT + " INTEGER" + ")";
	
	// MagneticField table create statement
	private static final String CREATE_TABLE_MagneticField= "CREATE TABLE "
			+ TABLE_MagneticField + "(" + KEY_ID + " INTEGER PRIMARY KEY," 
			+ KEY_mX + " FLOAT," 
			+ KEY_mY + " FLOAT,"
			+ KEY_mZ + " FLOAT,"
			+ KEY_activity + " INTEGER," 
			+ KEY_CREATED_AT + " INTEGER" + ")";
	
	// Barometer table create statement
	private static final String CREATE_TABLE_Barometer= "CREATE TABLE "
			+ TABLE_Barometer + "(" + KEY_ID + " INTEGER PRIMARY KEY," 
			+ KEY_baro + " FLOAT," 
			+ KEY_activity + " INTEGER," 
			+ KEY_CREATED_AT + " INTEGER" + ")";

	public DbHelper(Context context) {
		//super(context,  Environment.getExternalStorageDirectory() + File.separator+ "sdcard" + File.separator+ DATABASE_NAME, null, DATABASE_VERSION);
		super(context, DATABASE_NAME, null, DATABASE_VERSION);
		
		//SQLiteDatabase.openOrCreateDatabase( Environment.getExternalStorageDirectory() +"/sdcard/"+DATABASE_NAME,null);
	}

	@Override
	public void onCreate(SQLiteDatabase db) {
		Log.i("michelle~~~~~~~~~~~~","create DBHELPER~~~~~~~~~~~~~~~~~~");
		// creating required tables
		db.execSQL(CREATE_TABLE_Accelerometer);
		Log.i("michelle~~~~~~~~~~~~","created acc table~~~~~~~~~~~~~~~~~~");
		db.execSQL(CREATE_TABLE_Gyroscope);
		Log.i("michelle~~~~~~~~~~~~","created gyro table~~~~~~~~~~~~~~~~~~");
		db.execSQL(CREATE_TABLE_Barometer);
		db.execSQL(CREATE_TABLE_LinearAcc);
		db.execSQL(CREATE_TABLE_MagneticField);
	}

	@Override
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
		// on upgrade drop older tables
		db.execSQL("DROP TABLE IF EXISTS " + TABLE_Accelerometer);
		db.execSQL("DROP TABLE IF EXISTS " + TABLE_Barometer);
		db.execSQL("DROP TABLE IF EXISTS " + TABLE_Gyroscope);
		db.execSQL("DROP TABLE IF EXISTS " + TABLE_LinearAcc);
		db.execSQL("DROP TABLE IF EXISTS " + TABLE_MagneticField);
		// create new tables
		onCreate(db);
	}

	// ------------------------ "Accelerometer" table methods ----------------//

	/*
	 * Creating a Acc
	 */
	public void createAcc(AccelerometerDetails acc){
		SQLiteDatabase db = this.getWritableDatabase();
		Log.i("michelle~~~~~~~~~~~~","add row acc~~~~~~~~~~~~~~~~~~");
		ContentValues values = new ContentValues();
		values.put (KEY_accX, acc.getAccX());
		values.put (KEY_accY, acc.getAccY());
		values.put (KEY_accZ, acc.getAccZ());
		values.put(KEY_activity, acc.getActivityType());
		values.put (KEY_CREATED_AT,  System.currentTimeMillis());

		// insert row
		db.insert(TABLE_Accelerometer, null, values);
		db.close();
	}
	
	// ------------------------ "LinearAcc" table methods ----------------//

	/*
	 * Creating a LinearAcc
	 */
	public void createLinearAcc(LinearAccDetails acc) {
		Log.i("michelle~~~~~~~~~~~~","add row linear acc~~~~~~~~~~~~~~~~~~");
		SQLiteDatabase db = this.getWritableDatabase();

		ContentValues values = new ContentValues();
		values.put (KEY_laccX, acc.getLinearAccX());
		values.put (KEY_laccY, acc.getLinearAccY());
		values.put (KEY_laccZ, acc.getLinearAccZ());
		values.put(KEY_activity, acc.getActivityType());
		values.put (KEY_CREATED_AT,  System.currentTimeMillis());

		// insert row
		db.insert(TABLE_LinearAcc, null, values);
		db.close();
	}
	
	// ------------------------ "Gyroscope" table methods ----------------//

	/*
	 * Creating a Gyroscope
	 */
	public void createGyro(GyroscopeDetails acc) {
		SQLiteDatabase db = this.getWritableDatabase();
		Log.i("michelle~~~~~~~~~~~~","add row gyro~~~~~~~~~~~~~~~~~~");
		ContentValues values = new ContentValues();
		values.put (KEY_gX, acc.getGyroX());
		values.put (KEY_gY, acc.getGyroY());
		values.put (KEY_gZ, acc.getGyroZ());
		values.put(KEY_activity, acc.getActivityType());
		values.put (KEY_CREATED_AT,  System.currentTimeMillis());

		// insert row
		db.insert(TABLE_Gyroscope, null, values);
		db.close();
	}	
	
	// ------------------------ "MagneticField" table methods ----------------//

	/*
	 * Creating a MagneticField
	 */
	public void createMag(MagneticFieldDetails acc) {
		SQLiteDatabase db = this.getWritableDatabase();
		Log.i("michelle~~~~~~~~~~~~","add row mag~~~~~~~~~~~~~~~~~~");
		ContentValues values = new ContentValues();
		values.put (KEY_mX, acc.getMagX());
		values.put (KEY_mY, acc.getMagY());
		values.put (KEY_mZ, acc.getMagZ());
		values.put(KEY_activity, acc.getActivityType());
		values.put (KEY_CREATED_AT,  System.currentTimeMillis());

		// insert row
		db.insert(TABLE_MagneticField, null, values);
		db.close();
	}
	
	// ------------------------ "Barometer" table methods ----------------//

	/*
	 * Creating a Barometer
	 */
	public void createBaro(BarometerDetails acc) {
		SQLiteDatabase db = this.getWritableDatabase();
		Log.i("michelle~~~~~~~~~~~~","add row baro~~~~~~~~~~~~~~~~~~");
		ContentValues values = new ContentValues();
		values.put (KEY_baro, acc.getPressure());
		values.put(KEY_activity, acc.getActivityType());
		values.put (KEY_CREATED_AT,  System.currentTimeMillis());

		// insert row
		db.insert(TABLE_Barometer, null, values);
		db.close();
	}
	
	// closing database
	public void closeDB() {
		SQLiteDatabase db = this.getReadableDatabase();
		if (db != null && db.isOpen())
			db.close();
	}
	

}
