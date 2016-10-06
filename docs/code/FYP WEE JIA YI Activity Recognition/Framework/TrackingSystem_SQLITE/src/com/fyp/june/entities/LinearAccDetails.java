package com.fyp.june.entities;

import java.util.Date;

public class LinearAccDetails {
	private float linearAccX;
	private float linearAccY;
	private float linearAccZ;
	private Date dateNow;
	private int activityType;
	
	
	public LinearAccDetails(float linearAccX, float linearAccY, float linearAccZ, Date dateNow) {
		super();
		this.linearAccX = linearAccX;
		this.linearAccY = linearAccY;
		this.linearAccZ = linearAccZ;
		this.dateNow = dateNow;
	}

	public LinearAccDetails(float linearAccX, float linearAccY, float linearAccZ,
			Date dateNow, int activityType) {
		super();
		this.linearAccX = linearAccX;
		this.linearAccY = linearAccY;
		this.linearAccZ = linearAccZ;
		this.dateNow = dateNow;
		this.activityType = activityType;
	}
	
	public float getLinearAccX() {
		return linearAccX;
	}
	public void setLinearAccX(float linearAccX) {
		this.linearAccX = linearAccX;
	}
	public float getLinearAccY() {
		return linearAccY;
	}
	public void setLinearAccY(float linearAccY) {
		this.linearAccY = linearAccY;
	}
	public float getLinearAccZ() {
		return linearAccZ;
	}
	public void setLinearAccZ(float linearAccZ) {
		this.linearAccZ = linearAccZ;
	}
	public Date getDateNow() {
		return dateNow;
	}
	public void setDateNow(Date dateNow) {
		this.dateNow = dateNow;
	}
	public int getActivityType() {
		return activityType;
	}
	public void setActivityType(int activityType) {
		this.activityType = activityType;
	}
	
	
}
