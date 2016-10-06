import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

//note that acceleration and barometer readings use the same input class
//hence raw barometer readings have to be padded with 2 extra columns of zeros to get the same dimension as acc readings

public class MainClass {
	
	static ArrayList<ActivityTag> activitytagData =new ArrayList<ActivityTag>();
	static ArrayList<RawInput> rawInput =new ArrayList<RawInput>();

	//22 array lists for 22 different motion transitions
	static ArrayList<ProcessedInput> processedInput1 = new ArrayList<ProcessedInput>(); //Lying Down
	static ArrayList<ProcessedInput> processedInput2 = new ArrayList<ProcessedInput>(); //Sitting
	static ArrayList<ProcessedInput> processedInput3 = new ArrayList<ProcessedInput>(); //Standing
	static ArrayList<ProcessedInput> processedInput4 = new ArrayList<ProcessedInput>(); //Walking
	static ArrayList<ProcessedInput> processedInput5 = new ArrayList<ProcessedInput>(); //Running
	static ArrayList<ProcessedInput> processedInput61 = new ArrayList<ProcessedInput>(); //Fall from standing
	static ArrayList<ProcessedInput> processedInput62 = new ArrayList<ProcessedInput>(); //Fall from sitting
	static ArrayList<ProcessedInput> processedInput63 = new ArrayList<ProcessedInput>(); //Fall from walking
	static ArrayList<ProcessedInput> processedInput64 = new ArrayList<ProcessedInput>(); //Fall from running
	static ArrayList<ProcessedInput> processedInput7 = new ArrayList<ProcessedInput>(); //Sitting->Lying
	static ArrayList<ProcessedInput> processedInput8 = new ArrayList<ProcessedInput>(); //Lying->Sitting
	static ArrayList<ProcessedInput> processedInput9 = new ArrayList<ProcessedInput>(); //Sitting->Standing
	static ArrayList<ProcessedInput> processedInput10 = new ArrayList<ProcessedInput>(); //Standing->Sitting
	static ArrayList<ProcessedInput> processedInput11 = new ArrayList<ProcessedInput>(); //Walking->Sitting
	static ArrayList<ProcessedInput> processedInput12 = new ArrayList<ProcessedInput>(); //Sitting->Walking
	static ArrayList<ProcessedInput> processedInput13 = new ArrayList<ProcessedInput>(); //Walking->Lying
	static ArrayList<ProcessedInput> processedInput14 = new ArrayList<ProcessedInput>(); //Lying->Walking
	static ArrayList<ProcessedInput> processedInput15 = new ArrayList<ProcessedInput>(); //Walking->Standing
	static ArrayList<ProcessedInput> processedInput16 = new ArrayList<ProcessedInput>(); //Standing->Walking
	static ArrayList<ProcessedInput> processedInput17 = new ArrayList<ProcessedInput>(); //Standing->Lying
	static ArrayList<ProcessedInput> processedInput18 = new ArrayList<ProcessedInput>(); //Lying->Standing
	static ArrayList<ProcessedInput> processedInput19 = new ArrayList<ProcessedInput>(); //Standing->Running
	static ArrayList<ProcessedInput> processedInput20 = new ArrayList<ProcessedInput>(); //Running->Standing
	static ArrayList<ProcessedInput> processedInput21 = new ArrayList<ProcessedInput>(); //Walking->Running
	static ArrayList<ProcessedInput> processedInput22 = new ArrayList<ProcessedInput>(); //Running->Walking
	
	//this function loads the activity tag file
	//we need to manually create the tag file from the accelerometer raw inputs
	//we also need to manually ensure that the barometer raw inputs correspond to the same tag file, 
	//by adjusting the start end time-stamp of an activity
	public static void loadActivityTag (String fileName){
		try {
			Scanner in = new Scanner(new File(fileName));
			while (in.hasNext()) {
				String timeStart = in.next();
				String timeEnd = in.next();
				String activity = in.next();

				long tS = Long.parseLong(timeStart);
				long tE = Long.parseLong(timeEnd);
				int act = Integer.parseInt(activity);

				activitytagData.add(new ActivityTag(tS, tE, act));
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}
	
	//this function load the data input file 
	public static void loadData(String fileName) {
		try {
			Scanner in = new Scanner(new File(fileName));
			while (in.hasNext()){
				String timeStart = in.next();
				String tempX = in.next();
				String tempY = in.next(); //in the case of barometer readings Y and Z values will be 0
				String tempZ = in.next();
				String activity = in.next();

				long tS = Long.parseLong(timeStart);
				double x = Double.parseDouble(tempX);
				double y = Double.parseDouble(tempY);
				double z = Double.parseDouble(tempZ);
				int act = Integer.parseInt(activity);

				rawInput.add(new RawInput(tS, x, y, z, act));
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	//write processed input into different files, according to the activity type
	public static void writeToFile() throws IOException {
		BufferedWriter writer1 = new BufferedWriter(new FileWriter("111Laying.csv"));
		BufferedWriter writer2 = new BufferedWriter(new FileWriter("222Sit.csv"));
		BufferedWriter writer3 = new BufferedWriter(new FileWriter("333Stand.csv"));
		BufferedWriter writer4 = new BufferedWriter(new FileWriter("444Walk.csv"));
		BufferedWriter writer5 = new BufferedWriter(new FileWriter("555Run.csv"));
		BufferedWriter writer61 = new BufferedWriter(new FileWriter("61Fall.csv"));
		BufferedWriter writer62 = new BufferedWriter(new FileWriter("62Fall.csv"));
		BufferedWriter writer63 = new BufferedWriter(new FileWriter("63Fall.csv"));
		BufferedWriter writer64 = new BufferedWriter(new FileWriter("64Fall.csv"));
		BufferedWriter writer7 = new BufferedWriter(new FileWriter("777SitLying.csv"));
		BufferedWriter writer8 = new BufferedWriter(new FileWriter("888LyingSit.csv"));
		BufferedWriter writer9 = new BufferedWriter(new FileWriter("999SitStand.csv"));
		BufferedWriter writer10 = new BufferedWriter(new FileWriter("100StandSit.csv"));
		BufferedWriter writer11 = new BufferedWriter(new FileWriter("110WalkSit.csv"));
		BufferedWriter writer12 = new BufferedWriter(new FileWriter("120SitWalk.csv"));
		BufferedWriter writer13 = new BufferedWriter(new FileWriter("130WalkLying.csv"));
		BufferedWriter writer14 = new BufferedWriter(new FileWriter("140LyingWalk.csv"));
		BufferedWriter writer15 = new BufferedWriter(new FileWriter("150WalkStand.csv"));
		BufferedWriter writer16 = new BufferedWriter(new FileWriter("160StandWalk.csv"));
		BufferedWriter writer17 = new BufferedWriter(new FileWriter("170StandLying.csv"));
		BufferedWriter writer18 = new BufferedWriter(new FileWriter("180LyingStand.csv"));
		BufferedWriter writer19 = new BufferedWriter(new FileWriter("190StandRun.csv"));
		BufferedWriter writer20 = new BufferedWriter(new FileWriter("200RunStand.csv"));
		BufferedWriter writer21 = new BufferedWriter(new FileWriter("210WalkRun.csv"));
		BufferedWriter writer22 = new BufferedWriter(new FileWriter("220RunWalk.csv"));

		try {
			for (int item = 0; item < processedInput1.size(); item++){
				writer1.write(String.valueOf(processedInput1.get(item).getTimeStart()));
				writer1.write("\t");
				writer1.write(String.valueOf(processedInput1.get(item).getX()));
				writer1.write("\t");
				writer1.write(String.valueOf(processedInput1.get(item).getY()));
				writer1.write("\t");
				writer1.write(String.valueOf(processedInput1.get(item).getZ()));
				writer1.write("\t");
				writer1.write(String.valueOf(processedInput1.get(item).getCal()));
				writer1.newLine();
				writer1.flush();
			}

			for (int item = 0; item < processedInput2.size(); item++){
				writer2.write(String.valueOf(processedInput2.get(item).getTimeStart()));
				writer2.write("\t");
				writer2.write(String.valueOf(processedInput2.get(item).getX()));
				writer2.write("\t");
				writer2.write(String.valueOf(processedInput2.get(item).getY()));
				writer2.write("\t");
				writer2.write(String.valueOf(processedInput2.get(item).getZ()));
				writer2.write("\t");
				writer2.write(String.valueOf(processedInput2.get(item).getCal()));
				writer2.newLine();
				writer2.flush();
			}

			for (int item = 0; item < processedInput3.size(); item++){
				writer3.write(String.valueOf(processedInput3.get(item).getTimeStart()));
				writer3.write("\t");
				writer3.write(String.valueOf(processedInput3.get(item).getX()));
				writer3.write("\t");
				writer3.write(String.valueOf(processedInput3.get(item).getY()));
				writer3.write("\t");
				writer3.write(String.valueOf(processedInput3.get(item).getZ()));
				writer3.write("\t");
				writer3.write(String.valueOf(processedInput3.get(item).getCal()));
				writer3.newLine();
				writer3.flush();
			}

			for (int item = 0; item < processedInput4.size(); item++){
				writer4.write(String.valueOf(processedInput4.get(item).getTimeStart()));
				writer4.write("\t");
				writer4.write(String.valueOf(processedInput4.get(item).getX()));
				writer4.write("\t");
				writer4.write(String.valueOf(processedInput4.get(item).getY()));
				writer4.write("\t");
				writer4.write(String.valueOf(processedInput4.get(item).getZ()));
				writer4.write("\t");
				writer4.write(String.valueOf(processedInput4.get(item).getCal()));
				writer4.newLine();
				writer4.flush();
			}

			for (int item=0; item<processedInput5.size(); item++){
				writer5.write(String.valueOf(processedInput5.get(item).getTimeStart()));
				writer5.write("\t");
				writer5.write(String.valueOf(processedInput5.get(item).getX()));
				writer5.write("\t");
				writer5.write(String.valueOf(processedInput5.get(item).getY()));
				writer5.write("\t");
				writer5.write(String.valueOf(processedInput5.get(item).getZ()));
				writer5.write("\t");
				writer5.write(String.valueOf(processedInput5.get(item).getCal()));
				writer5.newLine();
				writer5.flush();
			}

			for (int item=0; item<processedInput61.size(); item++){
				writer61.write(String.valueOf(processedInput61.get(item).getTimeStart()));
				writer61.write("\t");
				writer61.write(String.valueOf(processedInput61.get(item).getX()));
				writer61.write("\t");
				writer61.write(String.valueOf(processedInput61.get(item).getY()));
				writer61.write("\t");
				writer61.write(String.valueOf(processedInput61.get(item).getZ()));
				writer61.write("\t");
				writer61.write(String.valueOf(processedInput61.get(item).getCal()));
				writer61.newLine();
				writer61.flush();
			}

			for (int item=0; item<processedInput62.size(); item++){
				writer62.write(String.valueOf(processedInput62.get(item).getTimeStart()));
				writer62.write("\t");
				writer62.write(String.valueOf(processedInput62.get(item).getX()));
				writer62.write("\t");
				writer62.write(String.valueOf(processedInput62.get(item).getY()));
				writer62.write("\t");
				writer62.write(String.valueOf(processedInput62.get(item).getZ()));
				writer62.write("\t");
				writer62.write(String.valueOf(processedInput62.get(item).getCal()));
				writer62.newLine();
				writer62.flush();
			}

			for (int item=0; item<processedInput63.size(); item++){
				writer63.write(String.valueOf(processedInput63.get(item).getTimeStart()));
				writer63.write("\t");
				writer63.write(String.valueOf(processedInput63.get(item).getX()));
				writer63.write("\t");
				writer63.write(String.valueOf(processedInput63.get(item).getY()));
				writer63.write("\t");
				writer63.write(String.valueOf(processedInput63.get(item).getZ()));
				writer63.write("\t");
				writer63.write(String.valueOf(processedInput63.get(item).getCal()));
				writer63.newLine();
				writer63.flush();
			}

			for (int item=0; item<processedInput64.size(); item++){
				writer64.write(String.valueOf(processedInput64.get(item).getTimeStart()));
				writer64.write("\t");
				writer64.write(String.valueOf(processedInput64.get(item).getX()));
				writer64.write("\t");
				writer64.write(String.valueOf(processedInput64.get(item).getY()));
				writer64.write("\t");
				writer64.write(String.valueOf(processedInput64.get(item).getZ()));
				writer64.write("\t");
				writer64.write(String.valueOf(processedInput64.get(item).getCal()));
				writer64.newLine();
				writer64.flush();
			}

			for (int item=0; item<processedInput7.size(); item++){
				writer7.write(String.valueOf(processedInput7.get(item).getTimeStart()));
				writer7.write("\t");
				writer7.write(String.valueOf(processedInput7.get(item).getX()));
				writer7.write("\t");
				writer7.write(String.valueOf(processedInput7.get(item).getY()));
				writer7.write("\t");
				writer7.write(String.valueOf(processedInput7.get(item).getZ()));
				writer7.write("\t");
				writer7.write(String.valueOf(processedInput7.get(item).getCal()));
				writer7.newLine();
				writer7.flush();
			}

			for (int item=0; item<processedInput8.size(); item++){
				writer8.write(String.valueOf(processedInput8.get(item).getTimeStart()));
				writer8.write("\t");
				writer8.write(String.valueOf(processedInput8.get(item).getX()));
				writer8.write("\t");
				writer8.write(String.valueOf(processedInput8.get(item).getY()));
				writer8.write("\t");
				writer8.write(String.valueOf(processedInput8.get(item).getZ()));
				writer8.write("\t");
				writer8.write(String.valueOf(processedInput8.get(item).getCal()));
				writer8.newLine();
				writer8.flush();
			}

			for (int item=0; item<processedInput9.size(); item++){
				writer9.write(String.valueOf(processedInput9.get(item).getTimeStart()));
				writer9.write("\t");
				writer9.write(String.valueOf(processedInput9.get(item).getX()));
				writer9.write("\t");
				writer9.write(String.valueOf(processedInput9.get(item).getY()));
				writer9.write("\t");
				writer9.write(String.valueOf(processedInput9.get(item).getZ()));
				writer9.write("\t");
				writer9.write(String.valueOf(processedInput9.get(item).getCal()));
				writer9.newLine();
				writer9.flush();
			}

			for (int item=0; item<processedInput10.size(); item++){
				writer10.write(String.valueOf(processedInput10.get(item).getTimeStart()));
				writer10.write("\t");
				writer10.write(String.valueOf(processedInput10.get(item).getX()));
				writer10.write("\t");
				writer10.write(String.valueOf(processedInput10.get(item).getY()));
				writer10.write("\t");
				writer10.write(String.valueOf(processedInput10.get(item).getZ()));
				writer10.write("\t");
				writer10.write(String.valueOf(processedInput10.get(item).getCal()));
				writer10.newLine();
				writer10.flush();
			}

			for (int item=0; item<processedInput11.size(); item++){
				writer11.write(String.valueOf(processedInput11.get(item).getTimeStart()));
				writer11.write("\t");
				writer11.write(String.valueOf(processedInput11.get(item).getX()));
				writer11.write("\t");
				writer11.write(String.valueOf(processedInput11.get(item).getY()));
				writer11.write("\t");
				writer11.write(String.valueOf(processedInput11.get(item).getZ()));
				writer11.write("\t");
				writer11.write(String.valueOf(processedInput11.get(item).getCal()));
				writer11.newLine();
				writer11.flush();
			}

			for (int item=0; item<processedInput12.size(); item++){
				writer12.write(String.valueOf(processedInput12.get(item).getTimeStart()));
				writer12.write("\t");
				writer12.write(String.valueOf(processedInput12.get(item).getX()));
				writer12.write("\t");
				writer12.write(String.valueOf(processedInput12.get(item).getY()));
				writer12.write("\t");
				writer12.write(String.valueOf(processedInput12.get(item).getZ()));
				writer12.write("\t");
				writer12.write(String.valueOf(processedInput12.get(item).getCal()));
				writer12.newLine();
				writer12.flush();
			}

			for (int item=0; item<processedInput13.size(); item++){
				writer13.write(String.valueOf(processedInput13.get(item).getTimeStart()));
				writer13.write("\t");
				writer13.write(String.valueOf(processedInput13.get(item).getX()));
				writer13.write("\t");
				writer13.write(String.valueOf(processedInput13.get(item).getY()));
				writer13.write("\t");
				writer13.write(String.valueOf(processedInput13.get(item).getZ()));
				writer13.write("\t");
				writer13.write(String.valueOf(processedInput13.get(item).getCal()));
				writer13.newLine();
				writer13.flush();
			}

			for (int item=0; item<processedInput14.size(); item++){
				writer14.write(String.valueOf(processedInput14.get(item).getTimeStart()));
				writer14.write("\t");
				writer14.write(String.valueOf(processedInput14.get(item).getX()));
				writer14.write("\t");
				writer14.write(String.valueOf(processedInput14.get(item).getY()));
				writer14.write("\t");
				writer14.write(String.valueOf(processedInput14.get(item).getZ()));
				writer14.write("\t");
				writer14.write(String.valueOf(processedInput14.get(item).getCal()));
				writer14.newLine();
				writer14.flush();
			}

			for (int item=0; item<processedInput15.size(); item++){
				writer15.write(String.valueOf(processedInput15.get(item).getTimeStart()));
				writer15.write("\t");
				writer15.write(String.valueOf(processedInput15.get(item).getX()));
				writer15.write("\t");
				writer15.write(String.valueOf(processedInput15.get(item).getY()));
				writer15.write("\t");
				writer15.write(String.valueOf(processedInput15.get(item).getZ()));
				writer15.write("\t");
				writer15.write(String.valueOf(processedInput15.get(item).getCal()));
				writer15.newLine();
				writer15.flush();
			}

			for (int item=0; item<processedInput16.size(); item++){
				writer16.write(String.valueOf(processedInput16.get(item).getTimeStart()));
				writer16.write("\t");
				writer16.write(String.valueOf(processedInput16.get(item).getX()));
				writer16.write("\t");
				writer16.write(String.valueOf(processedInput16.get(item).getY()));
				writer16.write("\t");
				writer16.write(String.valueOf(processedInput16.get(item).getZ()));
				writer16.write("\t");
				writer16.write(String.valueOf(processedInput16.get(item).getCal()));
				writer16.newLine();
				writer16.flush();
			}

			for (int item=0; item<processedInput17.size(); item++){
				writer17.write(String.valueOf(processedInput17.get(item).getTimeStart()));
				writer17.write("\t");
				writer17.write(String.valueOf(processedInput17.get(item).getX()));
				writer17.write("\t");
				writer17.write(String.valueOf(processedInput17.get(item).getY()));
				writer17.write("\t");
				writer17.write(String.valueOf(processedInput17.get(item).getZ()));
				writer17.write("\t");
				writer17.write(String.valueOf(processedInput17.get(item).getCal()));
				writer17.newLine();
				writer17.flush();
			}

			for (int item=0; item<processedInput18.size(); item++){
				writer18.write(String.valueOf(processedInput18.get(item).getTimeStart()));
				writer18.write("\t");
				writer18.write(String.valueOf(processedInput18.get(item).getX()));
				writer18.write("\t");
				writer18.write(String.valueOf(processedInput18.get(item).getY()));
				writer18.write("\t");
				writer18.write(String.valueOf(processedInput18.get(item).getZ()));
				writer18.write("\t");
				writer18.write(String.valueOf(processedInput18.get(item).getCal()));
				writer18.newLine();
				writer18.flush();
			}

			for (int item=0; item<processedInput19.size(); item++){
				writer19.write(String.valueOf(processedInput19.get(item).getTimeStart()));
				writer19.write("\t");
				writer19.write(String.valueOf(processedInput19.get(item).getX()));
				writer19.write("\t");
				writer19.write(String.valueOf(processedInput19.get(item).getY()));
				writer19.write("\t");
				writer19.write(String.valueOf(processedInput19.get(item).getZ()));
				writer19.write("\t");
				writer19.write(String.valueOf(processedInput19.get(item).getCal()));
				writer19.newLine();
				writer19.flush();
			}

			for (int item=0; item<processedInput20.size(); item++){
				writer20.write(String.valueOf(processedInput20.get(item).getTimeStart()));
				writer20.write("\t");
				writer20.write(String.valueOf(processedInput20.get(item).getX()));
				writer20.write("\t");
				writer20.write(String.valueOf(processedInput20.get(item).getY()));
				writer20.write("\t");
				writer20.write(String.valueOf(processedInput20.get(item).getZ()));
				writer20.write("\t");
				writer20.write(String.valueOf(processedInput20.get(item).getCal()));
				writer20.newLine();
				writer20.flush();
			}

			for (int item=0; item<processedInput21.size(); item++){
				writer21.write(String.valueOf(processedInput21.get(item).getTimeStart()));
				writer21.write("\t");
				writer21.write(String.valueOf(processedInput21.get(item).getX()));
				writer21.write("\t");
				writer21.write(String.valueOf(processedInput21.get(item).getY()));
				writer21.write("\t");
				writer21.write(String.valueOf(processedInput21.get(item).getZ()));
				writer21.write("\t");
				writer21.write(String.valueOf(processedInput21.get(item).getCal()));
				writer21.newLine();
				writer21.flush();
			}

			for (int item=0; item<processedInput22.size(); item++){
				writer22.write(String.valueOf(processedInput22.get(item).getTimeStart()));
				writer22.write("\t");
				writer22.write(String.valueOf(processedInput22.get(item).getX()));
				writer22.write("\t");
				writer22.write(String.valueOf(processedInput22.get(item).getY()));
				writer22.write("\t");
				writer22.write(String.valueOf(processedInput22.get(item).getZ()));
				writer22.write("\t");
				writer22.write(String.valueOf(processedInput22.get(item).getCal()));
				writer22.newLine();
				writer22.flush();
			}
		} catch (IOException ex) {
		    ex.printStackTrace();
		}finally{
			if (writer1 != null){
				writer1.close();
			}
			if (writer2!=null){
				writer2.close();
			}
			if (writer3!=null){
				writer3.close();
			}
			if (writer4!=null){
				writer4.close();
			}
			if (writer5!=null){
				writer5.close();
			}
			if (writer61!=null){
				writer61.close();
			}
			if (writer62!=null){
				writer62.close();
			}
			if (writer63!=null){
				writer63.close();
			}
			if (writer64!=null){
				writer64.close();
			}
			if (writer7!=null){
				writer7.close();
			}
			if (writer8!=null){
				writer8.close();
			}
			if (writer9!=null){
				writer9.close();
			}
			if (writer10!=null){
				writer10.close();
			}
			if (writer11!=null){
				writer11.close();
			}
			if (writer12!=null){
				writer12.close();
			}
			if (writer13!=null){
				writer13.close();
			}
			if (writer14!=null){
				writer14.close();
			}
			if (writer15!=null){
				writer15.close();
			}
			if (writer16!=null){
				writer16.close();
			}
			if (writer17!=null){
				writer17.close();
			}
			if (writer18!=null){
				writer18.close();
			}
			if (writer19!=null){
				writer19.close();
			}
			if (writer20!=null){
				writer20.close();
			}
			if (writer21!=null){
				writer21.close();
			}
			if (writer22!=null){
				writer22.close();
			}
		}
	}
	
	public static void preProcessingFunction(int interval) {
	    //in microseconds
		int accIndex = 0;

		//frequency = 100Hz -> period = 0.01s = 10ms
		for (int i = 0; i < activitytagData.size(); i++) {
			int rowCounter = 0;
			ActivityTag aT = activitytagData.get(i);
            ArrayList<RawInput> accSet = new ArrayList<RawInput>();

            long timeStart = aT.timeStart;
            long timeEnd = aT.timeEnd;
			long accTime = 0;

            // #3
			while (accTime < timeEnd) {
				accSet.add(new RawInput(rawInput.get(accIndex).getTimeStart(),
                                        rawInput.get(accIndex).getX(),
                                        rawInput.get(accIndex).getY(),
                                        rawInput.get(accIndex).getZ(),
                                        rawInput.get(accIndex).getAct())
                );

				accIndex++;
				if (accIndex < rawInput.size()) {
                    accTime = rawInput.get(accIndex).getTimeStart();
                } else {
                    break;
                }
			} 

            // #4 --> sampling
			for (long k = timeStart; k < timeEnd; k += interval){
				while (rowCounter < accSet.size() && accSet.get(rowCounter).getTimeStart() <= k){
					rowCounter++;
				}

				//get magnitude dimension
				double cal = Math.sqrt( (accSet.get(rowCounter - 1).getX() * accSet.get(rowCounter - 1).getX()) +
                                        (accSet.get(rowCounter - 1).getY() * accSet.get(rowCounter - 1).getY()) +
                                        (accSet.get(rowCounter - 1).getZ() * accSet.get(rowCounter - 1).getZ()));

				//sort data rows according to activity type
				switch(aT.activity) {
				case 1:
                    processedInput1.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 2:
                    processedInput2.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 3:
                    processedInput3.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 4:
                    processedInput4.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 5:
                    processedInput5.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 61:
                    processedInput61.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 62:
                    processedInput62.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 63:
                    processedInput63.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 64:
                    processedInput64.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 7:
                    processedInput7.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 8:
                    processedInput8.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 9:
                    processedInput9.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 0:
                    processedInput10.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 11:
                    processedInput11.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 12:
                    processedInput12.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 13:
                    processedInput13.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 14:
                    processedInput14.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 15:
                    processedInput15.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 16:
                    processedInput16.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 17:
                    processedInput17.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 18:
                    processedInput18.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 19:
                    processedInput19.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 20:
                    processedInput20.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 21:
                    processedInput21.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;

				case 22:
                     processedInput22.add(new ProcessedInput(k, accSet.get(rowCounter-1).getX(), accSet.get(rowCounter-1).getY(), accSet.get(rowCounter-1).getZ(), cal));
					break;
				}
			}
		}
	}

	
	public static void main(String[] arg) throws IOException{
		loadActivityTag ("popotag.txt");
		loadData ("popo.txt");

		//input sampling frequency here
		preProcessingFunction(100); //10Hz frequency
		writeToFile();
		System.out.println("DONE");
	}

}
