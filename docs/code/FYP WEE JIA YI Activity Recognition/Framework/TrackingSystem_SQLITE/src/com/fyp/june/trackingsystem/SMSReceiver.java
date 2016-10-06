package com.fyp.june.trackingsystem;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsMessage;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.widget.Toast;
/**
 * This class will receive a Toast message whenever an sms is received
 * @author Administrator
 *
 */
public class SMSReceiver extends BroadcastReceiver {

	@Override
	public void onReceive(Context context, Intent intent) {
	    // TODO Auto-generated method stub
		Log.w("IncommingSMSReceiver", "SMS Received");
		Bundle extras = intent.getExtras();
		       Object[] pdus = (Object[]) extras.get("pdus");
		       TelephonyManager tm = (TelephonyManager) context.getSystemService(Context.TELEPHONY_SERVICE);
		       SmsMessage sms;

		       for (Object pdu : pdus) {
		           sms = SmsMessage.createFromPdu((byte[]) pdu);
		           Log.w("IncommingSMSReceiver", "SMS Stored");
		           Toast.makeText(context, "Received SMS from" + sms.getOriginatingAddress(), Toast.LENGTH_SHORT).show();
		           if(sms.getMessageBody().startsWith("JTS")){
		        	   Intent i = new Intent(context.getApplicationContext(), PopupAlert.class);
			           i.putExtra("smscontent", sms.getMessageBody());
			           i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
			    		context.getApplicationContext().startActivity(i);
		           }
		           
		       }
	}

}
