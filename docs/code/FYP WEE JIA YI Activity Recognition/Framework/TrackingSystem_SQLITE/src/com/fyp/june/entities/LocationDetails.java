package com.fyp.june.entities;

import java.util.Date;

public class LocationDetails {
	private double latitude;
	private double longitude;
	private double accuracy;
	private Date timeRecorded;
	
	public double getLatitude() {
		return latitude;
	}
	public LocationDetails(double latitude, double longitude, double accuracy,
			Date timeRecorded) {
		super();
		this.latitude = latitude;
		this.longitude = longitude;
		this.accuracy = accuracy;
		this.timeRecorded = timeRecorded;
	}
	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}
	public double getLongitude() {
		return longitude;
	}
	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}
	public double getAccuracy() {
		return accuracy;
	}
	public void setAccuracy(double accuracy) {
		this.accuracy = accuracy;
	}
	public Date getTimeRecorded() {
		return timeRecorded;
	}
	public void setTimeRecorded(Date timeRecorded) {
		this.timeRecorded = timeRecorded;
	}
	
	

}
