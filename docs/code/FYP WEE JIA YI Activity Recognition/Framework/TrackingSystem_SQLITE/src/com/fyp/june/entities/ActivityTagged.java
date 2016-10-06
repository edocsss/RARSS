package com.fyp.june.entities;

import java.util.Date;

public class ActivityTagged {
	private String activity;
	private Date timeStart;
	private Date timeEnd;
	
	public ActivityTagged(String activity, Date timeStart, Date timeEnd) {
		super();
		this.activity = activity;
		this.timeStart = timeStart;
		this.timeEnd = timeEnd;
	}
	public ActivityTagged() {
		super();
	}
	public String getActivity() {
		return activity;
	}
	public void setActivity(String activity) {
		this.activity = activity;
	}
	public Date getTimeStart() {
		return timeStart;
	}
	public void setTimeStart(Date timeStart) {
		this.timeStart = timeStart;
	}
	public Date getTimeEnd() {
		return timeStart;
	}
	public void setTimeEnd(Date timeEnd) {
		this.timeEnd = timeEnd;
	}
	
	
}
