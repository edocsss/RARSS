package com.fyp.june.trackingsystem;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class BReceiver extends BroadcastReceiver {

	@Override
	public void onReceive(Context context, Intent intent) {
		//start service when phone runs
		Intent startServiceIntent = new Intent(context,MainService.class);
		context.startService(startServiceIntent);
		
	    // TODO Auto-generated method stub
	}

}
