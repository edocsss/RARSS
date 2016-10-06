package com.fyp.june.entities;

import java.util.Date;

public class MagneticFieldDetails {
	private float magX;
	private float magY;
	private float magZ;
	private Date dateNow;
	private int activityType;
	
	
	public int getActivityType() {
		return activityType;
	}
	public MagneticFieldDetails(float magX, float magY, float magZ,
			Date dateNow, int activityType) {
		super();
		this.magX = magX;
		this.magY = magY;
		this.magZ = magZ;
		this.dateNow = dateNow;
		this.activityType = activityType;
	}
	public void setActivityType(int activityType) {
		this.activityType = activityType;
	}
	public MagneticFieldDetails(float magX, float magY, float magZ, Date dateNow) {
		super();
		this.magX = magX;
		this.magY = magY;
		this.magZ = magZ;
		this.dateNow = dateNow;
	}
	public Date getDateNow() {
		return dateNow;
	}
	public void setDateNow(Date dateNow) {
		this.dateNow = dateNow;
	}
	public MagneticFieldDetails() {
		super();
	}
	
	public float getMagX() {
		return magX;
	}
	public void setMagX(float magX) {
		this.magX = magX;
	}
	public float getMagY() {
		return magY;
	}
	public void setMagY(float magY) {
		this.magY = magY;
	}
	public float getMagZ() {
		return magZ;
	}
	public void setMagZ(float magZ) {
		this.magZ = magZ;
	}
	
	
	
}
