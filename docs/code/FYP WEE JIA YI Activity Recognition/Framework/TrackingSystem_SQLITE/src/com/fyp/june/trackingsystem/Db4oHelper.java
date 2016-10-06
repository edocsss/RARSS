package com.fyp.june.trackingsystem;

import java.io.IOException;
import android.content.Context;
import android.util.Log;
import com.db4o.Db4oEmbedded;
import com.db4o.ObjectContainer;
import com.db4o.config.EmbeddedConfiguration;

public class Db4oHelper {
	private static Db4oHelper singleton = null;
	private static ObjectContainer db = null;
	private static Context context; 
	protected Db4oHelper(){
	}
	public static Db4oHelper getInstance(Context context){
		if (singleton==null){
			singleton = new Db4oHelper();
			Db4oHelper.context = context;
		}
		return singleton;
	}
	public static ObjectContainer db() {
		try {
			if (db == null || db.ext().isClosed()) {
				db = Db4oEmbedded.openFile(dbConfig(), db4oDBFullPath(context));
				//We first load the initial data from the database
				//ExercisesLoader.load(context, db);                                         
			}
			return db;
		} catch (Exception ie) {
			Log.e(Db4oHelper.class.getName(), ie.toString());
			return null;
		}
	}
	
	/**
	    * Configure the behavior of the database
	    */
	    private static EmbeddedConfiguration dbConfig() throws IOException {
	           EmbeddedConfiguration configuration = Db4oEmbedded.newConfiguration();
	           return configuration;
	    }
	/**
	 * Returns the path for the database location
	 */
	private static String db4oDBFullPath(Context ctx) {
		return ctx.getDir("data", 0) + "/" + "fyp.db4o";
	}
	public Context getContext() {
		return context;
	}
	public Db4oHelper setContext(Context context) {
		this.context = context;
		return this;
	}
}