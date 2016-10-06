public class ActivityTag {
	protected long timeStart;
	protected long timeEnd;
	protected int activity;
	
	public ActivityTag(long timeStart, long timeEnd, int activity){
		this.activity = activity;
		this.timeEnd = timeEnd;
		this.timeStart = timeStart;
	}
}
