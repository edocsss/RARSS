package com.fyp.june.entities;

import java.util.Date;

public class AccelerometerDetails {
	private float accX;
	private float accY;
	private float accZ;
	private Date dateNow;
	private int activityType;
	
	public AccelerometerDetails(float accX, float accY, float accZ, Date dateNow) {
		super();
		this.accX = accX;
		this.accY = accY;
		this.accZ = accZ;
		this.dateNow = dateNow;
	}

	public AccelerometerDetails(float accX, float accY, float accZ,
			Date dateNow, int activityType) {
		super();
		this.accX = accX;
		this.accY = accY;
		this.accZ = accZ;
		this.dateNow = dateNow;
		this.activityType = activityType;
	}

	public int getActivityType() {
		return activityType;
	}

	public void setActivityType(int activityType) {
		this.activityType = activityType;
	}


	public Date getDateNow() {
		return dateNow;
	}

	public void setDateNow(Date dateNow) {
		this.dateNow = dateNow;
	}

	public float getAccX() {
		return accX;
	}

	public void setAccX(float accX) {
		this.accX = accX;
	}

	public float getAccY() {
		return accY;
	}

	public void setAccY(float accY) {
		this.accY = accY;
	}

	public float getAccZ() {
		return accZ;
	}

	public void setAccZ(float accZ) {
		this.accZ = accZ;
	}
	
}
