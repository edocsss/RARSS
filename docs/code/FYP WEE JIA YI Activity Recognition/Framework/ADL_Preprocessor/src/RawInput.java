
public class RawInput {
	protected long timeStart;
	protected double accX;
	protected double accY;
	protected double accZ;
	protected int activity;
	
	public RawInput(long timeStart, double accX, double accY, double accZ, int act){
		this.activity = act;
		this.accX = accX;
		this.accY = accY;
		this.accZ = accZ;
		this.timeStart = timeStart;
	}
	public long getTimeStart(){
		return this.timeStart;
	}

	public double getX(){
		return this.accX;
	}

	public double getY(){
		return this.accY;
	}

	public double getZ(){
		return this.accZ;
	}

	public int getAct(){
		return this.activity;
	}
}
