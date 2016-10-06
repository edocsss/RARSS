package com.fyp.june.entities;

import java.util.Date;

public class AmbientLightDetails {
	private float brightness;
	private float temperature;
	private Date dateNow;
	private int activityType;
	
	public AmbientLightDetails(float brightness, float temperature,
			Date dateNow, int activityType) {
		super();
		this.brightness = brightness;
		this.temperature = temperature;
		this.dateNow = dateNow;
		this.activityType = activityType;
	}

	public AmbientLightDetails(float brightness, float temperature, Date dateNow) {
		super();
		this.brightness = brightness;
		this.temperature = temperature;
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

	public float getBrightness() {
		return brightness;
	}

	public void setBrightness(float brightness) {
		this.brightness = brightness;
	}

	public float getTemperature() {
		return temperature;
	}

	public void setTemperature(float temperature) {
		this.temperature = temperature;
	}
	
}
