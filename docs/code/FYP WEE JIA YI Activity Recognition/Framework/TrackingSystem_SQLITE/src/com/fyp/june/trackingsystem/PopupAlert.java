package com.fyp.june.trackingsystem;

import java.util.Date;

import android.app.Activity;
import android.content.Context;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.Window;
import android.view.WindowManager;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.TextView.OnEditorActionListener;
import android.widget.Toast;

public class PopupAlert extends Activity {

	private Button btn1, btn2, btn3, btn4,btn5, btn6, btn7, btn8,btn9, btn10;
	private TextView tvQn, txtLearnMore, txtExtra;
	public void setupUI(){
		btn1 = (Button)findViewById(R.id.btn1);
		btn2 = (Button)findViewById(R.id.btn2);
		btn3 = (Button)findViewById(R.id.btn3);
		btn4 = (Button)findViewById(R.id.btn4);
		btn5 = (Button)findViewById(R.id.btn5);
		btn6 = (Button)findViewById(R.id.btn6);
		btn7 = (Button)findViewById(R.id.btn7);
		btn8 = (Button)findViewById(R.id.btn8);
		btn9 = (Button)findViewById(R.id.btn9);
		btn10 = (Button)findViewById(R.id.btn10);
		tvQn = (TextView)findViewById(R.id.tvQn);
		txtLearnMore = (EditText)findViewById(R.id.txtLearnMore);
		txtExtra = (EditText)findViewById(R.id.txtIpAddr);
		btn1.setVisibility(View.VISIBLE);
		btn2.setVisibility(View.VISIBLE);
		btn3.setVisibility(View.VISIBLE);
		btn4.setVisibility(View.VISIBLE);
		btn5.setVisibility(View.VISIBLE);
		btn6.setVisibility(View.VISIBLE);
		btn7.setVisibility(View.VISIBLE);
		btn8.setVisibility(View.VISIBLE);
		btn9.setVisibility(View.VISIBLE);
		btn10.setVisibility(View.VISIBLE);

	}
	
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
				
	    super.onCreate(savedInstanceState);
	    requestWindowFeature(Window.FEATURE_NO_TITLE);
	    setContentView(R.layout.activity_popup);
	    //getWindow().clearFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);
	    getWindow().setBackgroundDrawable(new ColorDrawable(0));
	    Bundle extras = getIntent().getExtras();
	    if(extras!=null&&extras.containsKey("smscontent")){
	    	String smsContent = extras.getString("smscontent", null);

	    	String[] buttonTexts = smsContent.split(",");
		    //((TextView)findViewById(R.id.tvQn)).setText(extras.getString("smscontent", "this is a test"));

		    ((Button)findViewById(R.id.btn1)).setText(buttonTexts[1]);
		    ((Button)findViewById(R.id.btn2)).setText(buttonTexts[2]);
		    ((Button)findViewById(R.id.btn3)).setText(buttonTexts[3]);
	    }

	    setupUI();
	    setupClickEvents();
	    detectDone();
	    //** set text for activity options.
	}
	
	 private void setupClickEvents(){
		 btn1.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				Toast.makeText(getApplicationContext(), btn1.getText(), Toast.LENGTH_SHORT).show();
				//To insert into db4o
				MainActivity.lastActivity = btn1.getText().toString();
				MainActivity.ma.sendToServer();
				//Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn1.getText().toString(),new Date()));
	            //Db4oHelper.getInstance(getApplicationContext()).db().close();
				finish();
			}
		});
		 
		 btn3.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					Toast.makeText(getApplicationContext(), btn3.getText().toString(), Toast.LENGTH_SHORT).show();
//					//Creating new object
//					ActivityTest at = new ActivityTest();
//					at.setActivity(btn3.getText().toString());
//					at.setDateNow(new Date());
//					//To insert into db4o
//					Db4oHelper.getInstance(getApplicationContext()).db().store(at);
//		            Db4oHelper.getInstance(getApplicationContext()).db().close();
					MainActivity.lastActivity = btn3.getText().toString();
					MainActivity.ma.sendToServer();
//					Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn3.getText().toString(),new Date()));
//		            Db4oHelper.getInstance(getApplicationContext()).db().close();
					finish();
				}
			});
		 
		 btn2.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					Toast.makeText(getApplicationContext(), btn2.getText(), Toast.LENGTH_SHORT).show();
					MainActivity.lastActivity = btn2.getText().toString();
					MainActivity.ma.sendToServer();
//					Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn2.getText().toString(),new Date()));
//		            Db4oHelper.getInstance(getApplicationContext()).db().close();
					finish();
				}
			});
		 
		 btn4.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					// TODO Auto-generated method stub
					//Toast.makeText(getApplicationContext(), "running", Toast.LENGTH_SHORT).show();
					//visible textbox
					btn1.setVisibility(View.INVISIBLE);
					btn2.setVisibility(View.INVISIBLE);
					btn3.setVisibility(View.INVISIBLE);
					btn4.setVisibility(View.INVISIBLE);
					txtLearnMore.setVisibility(View.VISIBLE);
					//Auto focus keyboard 
					((InputMethodManager)getSystemService(Context.INPUT_METHOD_SERVICE))
			        .showSoftInput(txtLearnMore, InputMethodManager.SHOW_FORCED);
					
					//test
					
				}
			}); 
		 
		 btn5.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					Toast.makeText(getApplicationContext(), btn5.getText(), Toast.LENGTH_SHORT).show();
					//To insert into db4o
					MainActivity.lastActivity = btn5.getText().toString();
					MainActivity.ma.sendToServer();
					//Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn1.getText().toString(),new Date()));
		            //Db4oHelper.getInstance(getApplicationContext()).db().close();
					finish();
				}
			});
		 
		 btn6.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					Toast.makeText(getApplicationContext(), btn6.getText(), Toast.LENGTH_SHORT).show();
					//To insert into db4o
					MainActivity.lastActivity = btn6.getText().toString();
					MainActivity.ma.sendToServer();
					//Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn1.getText().toString(),new Date()));
		            //Db4oHelper.getInstance(getApplicationContext()).db().close();
					finish();
				}
			});
		 
		 btn7.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					Toast.makeText(getApplicationContext(), btn7.getText(), Toast.LENGTH_SHORT).show();
					//To insert into db4o
					MainActivity.lastActivity = btn7.getText().toString();
					MainActivity.ma.sendToServer();
					//Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn1.getText().toString(),new Date()));
		            //Db4oHelper.getInstance(getApplicationContext()).db().close();
					finish();
				}
			});
		 
		 btn8.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					Toast.makeText(getApplicationContext(), btn8.getText(), Toast.LENGTH_SHORT).show();
					//To insert into db4o
					MainActivity.lastActivity = btn8.getText().toString();
					MainActivity.ma.sendToServer();
					//Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn1.getText().toString(),new Date()));
		            //Db4oHelper.getInstance(getApplicationContext()).db().close();
					finish();
				}
			});
		 
		 btn9.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					Toast.makeText(getApplicationContext(), btn9.getText(), Toast.LENGTH_SHORT).show();
					//To insert into db4o
					MainActivity.lastActivity = btn9.getText().toString();
					MainActivity.ma.sendToServer();
					//Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn1.getText().toString(),new Date()));
		            //Db4oHelper.getInstance(getApplicationContext()).db().close();
					finish();
				}
			});
		 
		 btn10.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					Toast.makeText(getApplicationContext(), btn10.getText(), Toast.LENGTH_SHORT).show();
					//To insert into db4o
					MainActivity.lastActivity = btn10.getText().toString();
					MainActivity.ma.sendToServer();
					//Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(btn1.getText().toString(),new Date()));
		            //Db4oHelper.getInstance(getApplicationContext()).db().close();
					finish();
				}
			});
		 
	 }
	 
	 public void detectDone(){
	 txtLearnMore.setOnEditorActionListener(new OnEditorActionListener() {
		 @Override
		    public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
		        if (actionId == EditorInfo.IME_ACTION_DONE) {
		            // do your stuff here
		        	Toast.makeText(getApplicationContext(), txtLearnMore.getEditableText().toString(), Toast.LENGTH_SHORT).show();
		        	
		        	if (!txtLearnMore.getEditableText().toString().equals("")){
//		        		Db4oHelper.getInstance(getApplicationContext()).db().store(new ActivityTest(txtLearnMore.getText().toString(),new Date()));
//		            	Db4oHelper.getInstance(getApplicationContext()).db().close();
		        		MainActivity.lastActivity = txtLearnMore.getEditableText().toString();
						MainActivity.ma.sendToServer();
		        		finish();
		        }
		        }
		        return false;
		    }
		});
	 
	 }
	 
	 

}
