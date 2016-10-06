import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import org.apache.commons.math.stat.descriptive.DescriptiveStatistics;

public class MainClass {
    private static final double SMA_THRESHOLD = 0.78;
    private static final double BAROMETER_THRESHOLD = 1.1;

    static DescriptiveStatistics SMA = new DescriptiveStatistics(); //use this to help retrieve standard deviation of given SMA values
	static DescriptiveStatistics BARO = new DescriptiveStatistics(); //use this to help retrieve sum of given barometer std dev values
	static ArrayList<inputClass> inputData =new ArrayList<inputClass>();
	
	public static void loadinput(String fileName) {
		try {
			Scanner in = new Scanner(new File(fileName));

			while (in.hasNext()) {
				String smaStr= in.next();
				String activityStr = in.next();
				String baroStr = in.next();

				double sma = Double.parseDouble(smaStr);
				int act = Integer.parseInt(activityStr);
				double baro = Double.parseDouble(baroStr);

				inputData.add(new inputClass(sma, act, baro));
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void writeoutput(ArrayList<inputClass> window) throws IOException{
		BufferedWriter writer1 = new BufferedWriter(new FileWriter("higherlevelmotion.csv"));
		try {
			for (int item = 0; item < window.size(); item++){
				writer1.write(String.valueOf(window.get(item).getact()));
				writer1.write("\t");
				writer1.newLine();
				writer1.flush();
			}
		} catch (IOException ex) {
		    ex.printStackTrace();
		} finally {
			if (writer1 != null) {
				writer1.close();
			}
		}
	}
	
	public static int motionTransitionRecognition(int index){
		boolean fallFlag;

		//make sure motion #5 is clean
        //find max of next 5 overlapping frames
		int maxKey = getMostFrequentActivityKeyInAWindow(index + 4);

        // Check the 5th item (a bit different from the report)
		if (inputData.get(index + 4).getact() != maxKey){
			System.out.printf("Last motion of index %d is cleaned up to be %d\n", index+4, maxKey);
			inputData.get(index + 4).setact(maxKey); //clean up motion 5
		}

        // The comparison is between the first and the last element
        // Because if the first and second element are different, then there is ONLY A MOTION TRANSITION
        // The 2 - 4 element is the transition movement (and hence it's not stable yet)
        // Once we know the 5th element, we can know what is the true transition (Sitting - Lying, etc.)
        // If the barometer reading changes drastically, then it is possibly a falling action
        // Basically, the three middle elements are only transition motion or unstable motions that we don't need to consider
		if (inputData.get(index + 4).getact() == 1){
			fallFlag = fallDetection(index); //possible falling
			if (inputData.get(index).getact() == 2){
				if (fallFlag) {
					System.out.printf("Index %d to %d has transition 62\n", index, index+4);
					return 62; //Fall(Sit)
				} else {
					System.out.printf("Index %d to %d has transition 7\n", index, index+4);
					return 7; //Sit->Lying
				}
			}
			else if (inputData.get(index).getact()==3){
				if (fallFlag){
					System.out.printf("Index %d to %d has transition 61\n", index, index+4);
					return 61; //Fall(Stand)
				}
				else{
					System.out.printf("Index %d to %d has transition 17\n", index, index+4);
					return 17; //Stand->Lying; 
				}
			}
			else if (inputData.get(index).getact()==4){
				if (fallFlag){
					System.out.printf("Index %d to %d has transition 63\n", index, index+4);
					return 63; //Fall(Walk)
				}
				else{
					System.out.printf("Index %d to %d has transition 13\n", index, index+4);
					return 13; //Walk->Lying; 
				}
			}
			else if (inputData.get(index).getact()==5){
				if (fallFlag){
					System.out.printf("Index %d to %d has transition 64\n", index, index+4);
					return 64; //Fall(Run)
				}
				else{
					System.out.printf("Index %d to %d has unknown transition\n", index, index+4);
					return 0; //unknown
				}
			}
		}
		else { //normal transitions
			if (inputData.get(index).getact()==1 && inputData.get(index+4).getact()==2) return 8; //Lying->Sit
			if (inputData.get(index).getact()==1 && inputData.get(index+4).getact()==4) return 14; //Lying->Walk
			if (inputData.get(index).getact()==1 && inputData.get(index+4).getact()==3) return 18; //Lying->Stand
			if (inputData.get(index).getact()==2 && inputData.get(index+4).getact()==3) return 9; //Sit->Stand
			if (inputData.get(index).getact()==2 && inputData.get(index+4).getact()==4) return 12; //Sit->Walk
			if (inputData.get(index).getact()==3 && inputData.get(index+4).getact()==2) return 10; //Stand->Sit
			if (inputData.get(index).getact()==3 && inputData.get(index+4).getact()==4) return 16; //Stand->Walk
			if (inputData.get(index).getact()==3 && inputData.get(index+4).getact()==5) return 19; //Stand->Run
			if (inputData.get(index).getact()==4 && inputData.get(index+4).getact()==2) return 11; //Walk->Sit
			if (inputData.get(index).getact()==4 && inputData.get(index+4).getact()==3) return 15; //Walk->Stand
			if (inputData.get(index).getact()==4 && inputData.get(index+4).getact()==5) return 21; //Walk->Run
			if (inputData.get(index).getact()==5 && inputData.get(index+4).getact()==3) return 20; //Run->Stand
			if (inputData.get(index).getact()==5 && inputData.get(index+4).getact()==4) return 22; //Run->Walk
			return 0; //unknown
		}

		return 0;
	}
	
	// to get the key that has the highest occurence in a window
	public static int getMostFrequentActivityKeyInAWindow(int index){
		int maxKey = 0;
	    int maxCounts = 0;
	    int[] counts = new int[30]; //possible no. of transition type

	    for (int i = 0; i < 5; i++) {
	        counts[inputData.get(index).getact()]++;
	        index++;

	        if (maxCounts < counts[inputData.get(index).getact()]) {
	            maxCounts = counts[inputData.get(index).getact()];
	            maxKey = inputData.get(index).getact();
	        }
	    }

	    return maxKey;
	}
	
	public static boolean fallDetection(int index) {
		 for (int i = 0; i < 5; i++) {
			 BARO.addValue(inputData.get(index + i).getbaro());
		 }

		 double sum= BARO.getSum();
		 if (sum > BAROMETER_THRESHOLD) { //Barometer threshold can be set here
			 return true;
		 } else {
             return false;
         }
	}
	
	// using majority voting
	public static void smoothing(int index) {
	    int maxKey = getMostFrequentActivityKeyInAWindow(index);

        //only smooth middle 3 actions
	    for (int i = 1; i < 4; i++) {
	    	if (inputData.get(index + i).getact() != maxKey) {
	    		System.out.printf("Smoothing index %d to be new motion %d\n", index, maxKey);
	    		inputData.get(index + i).setact(maxKey);
	    	}
	    }
	}

    // THE WINDOW CONCEPT USED HERE IS DIFFERENT FROM THAT IN SAMPLING PRE-PROCESSING PROCESS
	public static void main(String[] arg) throws IOException{
        int indexCount = 0;
        int results;

        loadinput("input.txt");
		try {
            while (indexCount < inputData.size() - 5) {
                // Check the first 2 data, if the two sequential motions are different,
                // then it is possible that there is a motion transition
                if (inputData.get(indexCount).getact() != inputData.get(indexCount + 1).getact()) {
                    System.out.printf("Index %d to %d has different motion\n", indexCount, indexCount + 1);

                    // If there is a POSSIBLE motion transition, calculate the 5 WINDOWS standard deviation
                    for (int i = 0; i < 5; i++) {
                        SMA.addValue(inputData.get(indexCount + i).getsma());
                    }


                    // TRUE TRANSITION
                    double stdev = SMA.getStandardDeviation();
                    if (stdev >  SMA_THRESHOLD) {
                        System.out.printf("Index %d to %d has transition\n", indexCount, indexCount + 4);
                        results = motionTransitionRecognition(indexCount); //return transition from m1 - m5

                        for (int transition = 1; transition < 4; transition++){
                            inputData.get(indexCount + transition).setact(results);
                        }
                    }

                    // FALSE TRANSITION
                    else {
                        System.out.printf("Index %d to %d has NO transition\n", indexCount, indexCount + 4);
                        smoothing(indexCount);
                    }

                    // Meaning that there is 1 window overlapping
                    indexCount += 4;
                } else {
                    System.out.printf("Index %d to %d has same motion\n", indexCount, indexCount + 1);
                    indexCount++;
                }
            }

            writeoutput(inputData);
		}
		catch (Exception e){
			System.out.println(e);
		}
	}	
}
