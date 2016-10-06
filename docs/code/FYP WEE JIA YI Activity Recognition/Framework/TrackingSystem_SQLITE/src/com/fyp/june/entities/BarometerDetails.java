package com.fyp.june.entities;

import java.util.Date;

public class BarometerDetails {
	private float pressure;
	private Date dateNow;
	private int activityType;
	
	public BarometerDetails(float pressure,
			Date dateNow, int activityType) {
		super();
		this.pressure = pressure;
		this.dateNow = dateNow;
		this.activityType = activityType;
	}

	public BarometerDetails(float pressure, Date dateNow) {
		super();
		this.pressure = pressure;
		this.dateNow = dateNow;
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

	public float getPressure(){
		return pressure;
	}

	public void setPressure(float pressure) {
		this.pressure = pressure;
	}


	
}
