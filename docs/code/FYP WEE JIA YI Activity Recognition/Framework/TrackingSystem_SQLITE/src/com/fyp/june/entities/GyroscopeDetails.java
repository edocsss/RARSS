package com.fyp.june.entities;

import java.util.Date;

public class GyroscopeDetails {
	private float gyroX;
	private float gyroY;
	private float gyroZ;
	private Date dateNow;
	private int activityType;
	
	public GyroscopeDetails(float gyroX, float gyroY, float gyroZ, Date dateNow) {
		super();
		this.gyroX = gyroX;
		this.gyroY = gyroY;
		this.gyroZ = gyroZ;
		this.dateNow = dateNow;
	}

	public GyroscopeDetails(float gyroX, float gyroY, float gyroZ,
			Date dateNow, int activityType) {
		super();
		this.gyroX = gyroX;
		this.gyroY = gyroY;
		this.gyroZ = gyroZ;
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

	public float getGyroX() {
		return gyroX;
	}

	public void setGyroX(float gyroX) {
		this.gyroX = gyroX;
	}

	public float getGyroY() {
		return gyroY;
	}

	public void setGyroY(float gyroY) {
		this.gyroY = gyroY;
	}

	public float getGyroZ() {
		return gyroZ;
	}

	public void setGyroZ(float gyroZ) {
		this.gyroZ = gyroZ;
	}
	
	
	
}
