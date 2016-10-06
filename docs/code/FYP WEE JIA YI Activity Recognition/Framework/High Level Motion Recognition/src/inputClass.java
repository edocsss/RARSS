public class inputClass {
	// input file should contain three data columns:
    // - SMA values
    // - low level prediction labels
    // - barometer standard deviation values

	protected double sma;
	protected int activity;
	protected double baro;
	
	public inputClass(double sma ,int activity, double baro) {
		this.activity = activity;
		this.sma = sma;
		this.baro= baro;
	}
	
	public double getsma(){
		return this.sma;
	}

	public int getact(){
		return this.activity;
	}

	public double getbaro(){
		return this.baro;
	}

	public void setbaro(double baro){
		this.baro=baro;
	}

	public void setsma(double sma){
		this.sma=sma;
	}

	public void setact(int act){
		this.activity=act;
	}
}
