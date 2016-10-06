package com.fyp.june.entities;

import java.util.ArrayList;
import java.util.Date;

public class ClientToServerContainer {
	public String uuid;
	public ArrayList<?> accArraylist;
	public ArrayList<?> gyroArraylist;
	public ArrayList<?> magArraylist;
	public ArrayList<?> linearArraylist;
	public ArrayList<?> barometerArraylist;
	public String activityType;
	public Date startTime = new Date();
	public Date endTime = new Date();
	
}
