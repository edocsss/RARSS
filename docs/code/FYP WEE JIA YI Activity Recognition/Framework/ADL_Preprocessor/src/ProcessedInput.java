
public class ProcessedInput {
	protected long timeStart;
	protected double accX;
	protected double accY;
	protected double accZ;
	protected double cal;
	
	public ProcessedInput(long timeStart, double x, double y, double z, double cal) {
		this.cal = cal;
		this.accX = x;
		this.accY = y;
		this.accZ = z;
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

	public double getCal(){
		return this.cal;
	}
}
