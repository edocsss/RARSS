# Requirements
1. Python 3.5
2. ```pip``` installed and in the path
3. All Python libraries mentioned in ```<path_to_server_root_dir>/requirements.txt``` installed. You can use ```pip install -r <path_to_server_root_dir>/requirements.txt``` to easily do this
4. Change the web server configuration if needed in ```<path_to_server_root_dir/webapp/web_config.py```
5. MongoDB 3.2.6
6. **[HIGHLY RECOMMENDED]** Install PyCharm and use it as the main Python IDE for this project (otherwise, you have to set the ```PYTHONPATH``` environment variable every time)

Please note that the documentation here will only discuss the steps needed using PyCharm IDE. If you choose not to use the PyCharm IDE, I would assume that you are confident enough using Python from your terminal and hence you know how Python behaves if the scripts are executed via a terminal. 



# Setting Up PyCharm
1. Import the ```<path_to_server_root_dir>``` folder to PyCharm
2. Make sure the path ```<path_to_server_root_dir>``` is set to be the ```source root```. Open ```Preferences - Project Structure```, set the path ```<path_to_server_root_dir>``` to be the ```Source Folder```.
3. The ```server``` folder icon should now be marked with a ```blue``` color if you see it at the sidebar!



# Running the Web Server
1. Run the MongoDB server (use the ```<path_to_server_root_dir>/run_mongod.sh``` script)
2. Simply run ```<path_to_server_root_dir>/webapp/tornado.py``` from the IDE
3. This will run the Web Server at the port specified in ```<path_to_server_root_dir>/webapp/web_config.py```



# Smartphone and Smarwatch Synchronization during Activity Recording
One issue with using Tizen Smartwatch is that the documention is not very good and hence I chose not to pair the Smartwatch and Smartphone via Bluetooth connection. In this project, I decided to use WebSocket to perform push notification from the server to the Smartwatch.

This section here will briefly discuss how the Smartphone and Smartwatch interact with each other so that when the activity recording is stopped, both devices can send the raw sensory data to the server correctly.

### Start Activity Recording
**IMPORTANT NOTE: MAKE SURE YOU CLOSE AND RE-OPEN THE SMARTWATCH APPLICATION BEFORE ANY RECORDING SESSION!!!**

The reason for doing this is because the timestamp recorded by the Smartwatch may not be correct (jumping timestamp) for the second recording session if the application is not closed. I have no idea why and decided to just close and re-open instead of investigating the root cause and spent too much time.

1. When the ```Start Recording``` button found in the Smartphone application, the Smartphone will send an HTTP request to the server and the server will notify the Smartwatch with sufficient information about the activity. The information sent is only the ```activity type``` being recorded.
2. The Smartphone will start recording the sensor readings.
3. The Smartwatch will receive this information via WebSocket, store the ```activity type``` locally, and start recording the sensor readings.

**PLEASE NOTE THAT THERE IS NO DELAY BETWEEN PRESSING THE START RECORDING BUTTON AND THE SENSOR READINGS RECORDING!!**

### Stop Activity Recording
1. When the ```Stop Recording``` button found in the Smartphone application is pressed **OR** the timer has ended, the Smartphone will stop recording the sensor readings immediately.
   - This will also notify the server and the server will notify the Smartwatch.
   - The Smartwatch will then stop recording the sensor readings as well (basically, it is the same mechanism as the `Start Activity Recording` section).
2. After pressing on the `Send Data` button in the Smartphone application, the application will bundle all the sensor readings and send it to the server via HTTP.
3. Once the server receives the data, the server re-formats the data and store the data to ```<path_to_server_root_dir>/data/raw```.
4. In order to differentiate between one recording session and another, **the Smartphone also keeps track a unique ID which will be incremented every time it sends data to the server**!!
5. The server will now **notify the Smartwatch** to send its data to the server. The notification includes the same **unique ID** the Smartphone used just now!
6. As soon as the Smartwatch receives the notification, it will send the data to the server and use the same **unique ID**!
7. The server receives the data, the server re-formats the data, and store the data to ```<path_to_server_root_dir>/data/raw```.



# Pre-processing Raw Data for Model Building
There are multiple important files for doing the data pre-processing:

1. ```<path_to_server_root_dir>/config.py```: includes **all** configuration needed for the pre-processing (sampling frequency, window size, whose data to use, folder names, file names, etc.)
2. ```<path_to_server_root_dir>/data_processor/data_sampler.py```: contains code for doing the data sampling based on the sampling frequency
3. ```<path_to_server_root_dir>/data_processor/data_window_selector.py```: contains code for doing the window segmentation based on the window size
4. ```<path_to_server_root_dir>/data_processor/feature_generator.py```: contains code for doing the features generation
5. ```<path_to_server_root_dir>/data_processor/data_combiner.py```: contains code for combining dataframe from different sensors and different device source
6. ```<path_to_server_root_dir>/data_processor/data_preprocessor.py```: the main trigger for the data pre-processing pipeline

In order to generate the combined and pre-processed data, the only thing you need to do is run the ```<path_to_server_root_dir>/data_processor/data_preprocessor.py```. 

This will take quite some time depending on how many activities you would like to pre-process and the configurations used. You can also specify the activities you would like to pre-process in the same Python file.

**Please take note that configurations such as the window size, sampling frequency, which test subject's data to preprocess, etc. can be found in ```<path_to_server_root_dir>/config.py```! Always check for the current configuration used before running the preprocessor!**

### Configuration
Please change the data pre-processing configurations in ```<path_to_server_root_dir>/config.py``` accordingly!

### Data Features
At the moment, we are only using the ```Accelerometer``` data (although data from other sensors are still recorded for just in case purpose) from both Smartphone and Smartwatch. The features generated for the Smartphone and Smartwatch are the same. The features considered are:

1. Mean
2. Variance
3. Covariance (all combinations between x-axis, y-axis, z-axis, and magnitude)
4. Energy
5. Entropy

For features other than the ```covariance```, they are applied to all 3-axes (x, y, and z) and the accelerometer magnitude (calculated in the server using the usual vector magnitude formula). In addition, the formula used for the ```Energy``` and ```Entropy``` can be found in Prof. Tan's and Dr. Wang's paper: **Non Intrusive Robust Human Activity Recognition for Diverse Age Groups**.



# Data Pre-processing Steps and Logics
This section will discuss the main ideas used in the data pre-processing and the different steps involved. Please read the code to better understand the logic details!

### Raw Data
The raw data read from the file system is returned in this format:
```
{
  'sp_accelerometer': [<DataItemObject_ForRecordingSession1>, <DataItemObject_ForRecordingSession2>, ...],
  'sw_accelerometer': [<DataItemObject_ForRecordingSession1>, <DataItemObject_ForRecordingSession2>, ...],
  'sp_<other_sensors>': [...],
  'sw_<other_sensors>': [...]
}
```

So, the `data sampling` and `data windowing` process are actually performed on **each** `DataItemObject` first before they are combined in later stages. 

### Data Sampling
One important thing to note here: although I mentioned that the sampling is done for each `DataItemObject`, it is **not fully** independent from other `DataItemObject` of the **same recording session**. This is because of the **timestamp synchronization** problem between the Smartphone and Smartwatch data.

For an Activity Recording session (raw data files with the same File ID), the starting and ending timestamp for each CSV file may not be the same. Thus, before the data sampling starts, the timestamps need to be normalized for each DataFrame. 

1. Subtract each row's timestamp with the first row's timestamp. Thus, the first timestamp of all `DataFrame` will always be 0.
2. Compare the ending timestamp (after subtracted with the first row's timestamp) and find the **earliest ending timestamp**.
3. Remove the outliers from the data by adding the starting timestamp with a constant (configurable) and the ending timestamp with a constant as well. Rows with timestamps that do not fall into the new timestamp interval will be discarded!

Now that the DataFrames have been normalized in terms of the timestamp, we can perform the data sampling. The idea of data sampling is to sample the data at a fixed timestamp interval depending on the sampling frequency. For example, if we have this data:
```
Timestamp (s) | Data
    1         |  31
    2         |  33
    4         |  35
    6         |  40
```

After timestamp normalization:
```
Timestamp (s) | Data
    0         |  31
    1         |  33
    3         |  35
    5         |  40
```

After sampling with the frequency of 0.25 Hz (1 data point per 4 seconds):
```
Timestamp (s) | Data
    0         |  31
    4         |  35 (use the last data although in the interval of [0, 4] there are 2 data points (33 and 35)
    8         |  40
```

After sampling with the frequency of 2 Hz (2 data points per second):
```
Timestamp (s) | Data
    0         |  31
    0.5       |  31
    1         |  33
    1.5       |  33
    2         |  33
    2.5       |  33
    3         |  35
    3.5       |  35
    4         |  35
    4.5       |  35
    5         |  40
    5.5       |  40
    6         |  40
```

Once data sampling is done, the result is still organized in the same manner as before it is sampled (similar to the one discussed in the `Raw Data` section but the data is now sampled).

### Data Windowing
Once the original raw data has been sampled at a fixed interval, it is divided into data frames of fixed window size. In addition, depending on the given configuration, frames may overlap with the previous and next frame. These configurations can be found in the `config.py` file.

For example, if we have this sampled data:
```
Timestamp (s) | Data
    0         |  31
    0.5       |  31
    1         |  33
    1.5       |  33
    2         |  33
    2.5       |  33
    3         |  35
    3.5       |  35
    4         |  35
    4.5       |  35
    5         |  40
    5.5       |  40
    6         |  40
```

We would like to perform Data Windowing with `window size = 2s` and `half overlapping`. The resulting windows would be:
**Window 1**:
```
Timestamp (s) | Data
    0         |  31
    0.5       |  31
    1         |  33
    1.5       |  33
```

**Window 2**:
```
Timestamp (s) | Data
    1         |  33
    1.5       |  33
    2         |  33
    2.5       |  33
```

**Window 3**:
```
Timestamp (s) | Data
    2         |  33
    2.5       |  33
    3         |  35
    3.5       |  35
```

and so on. Each data window/frame will be used for feature generation in later stage. This means each data window/frame will generate one set of features.

### Combine Windowed Data by the Device Source
At this point, for **an activity**, the raw data for **each sensor type** and **device source** has been divided into frames/windows. This step will combine the data windows from **different sensor type** by **the device source** into one combined dataset.

For example, if initially we have:

`sp_accelerometer`:
```
timestamp | ax | ay | az
...       | .. | .. | ..
```

`sp_gyrometer`:
```
timestamp | gx | gy | gz
...       | .. | .. | ..
```

`combined_smartphone`:
```
timestamp | ax | ay | az | gx | gy | gz
...       | .. | .. | .. | .. | .. | ..
```

The results of this step would be **1 combined dataset for Smartphone** and **1 combined dataset for Smartwatch**. Thus, each row of the **Smartphone dataset** will now have the raw data of the Smartphone sensors that you would like to consider in the feature generation (configurable in the `config.py`). The same logic applies for the Smartwatch.

### Generate Features
Once the raw data has been combined into one dataset for each device, we now need to generate features. As mentioned earlier, at the moment, only **accelerometer** data is used in this phase. The list of features generated can be seen from previous sections.

Please note that each data window/frame will generate **one data record of feature**!

### Combine Features Generated for Each Activity
This phase is similar to the previous phase of combining multiple datasets. At this phase, we have already generated two feature datasets, 1 for Smartphone and 1 for Smartwatch. We need to combine these two datasets into **one single dataset** and this will be the final combined dataset for **an activity**.

For example:

`sp_features`:
```
index | sp_mean_ax | sp_mean_ay| ...
1     |    ....    |    ....   | ...
2     |    ....    |    ....   | ...
```

`sw_features`:
```
index | sw_mean_ax | sw_mean_ay| ...
1     |    ....    |    ....   | ...
2     |    ....    |    ....   | ...
```

`combined_dataset_for_each_activity`:
```
index | sp_mean_ax | sp_mean_ay| sw_mean_ax | sw_mean_ay | ...
1     |    ....    |    ....   |    ....    |    ....    | ...
2     |    ....    |    ....   |    ....    |    ....    | ...
```

### Combine All Activities into One Full Dataset (per subject)
At this point, each subject will already have **one combined dataset for each activity**. The last thing to do is to combine those datasets into **one huge dataset** for **each subject**! We just need to append the rows of each activity's combined dataset altogether.


# Model K-Fold Cross Validation
All K-Fold CV related files can be found in ```<path_to_server_root_dir>/classifier/cv```.

### Data Pre-processing for Models
After features are generated and before building the model, there are some additional data pre-processings required.
1. Encoding the activity type with an integer
2. Normalizing each feature into [0, 1] range
3. **[Only for MLP]** Encoding the activity type using onehot method

### Model Configuration
Each model Python file will have a `__main__` part in which you can change the parameters related to each model. If you would like to change more general configurations like the `training size`, `testing size`, or `whose data to use for training and/or testing`, you can change those in ```<path_to_server_root_dir>/config.py```.

### Model Validation (K-Fold)
There are 4 models we are currently using: SVM, Random Forest, Naive Bayes, and Multi-Layer Perceptron (MLP). Model Validation using the K-Fold CV can be easily done by running the corresponding Python file. For example, if you would like to test SVM model, run  ```<path_to_server_root_dir>/classifier/cv/svm.py```.

Each model building Python script will have different possible parameters that you can play around with. In addition, the Python script also allows testing different parameter values (similar to Grid search, but not an exhaustive parameter search).

### Model Validation (Leave-One-Out)
The LOO configuration (training and testing dataset) can be found in `<path_to_server_root_dir>/config.py`. Other things inside the script are mostly the same as K-Fold CV. 

One additional parameter is the `permutate_xyz`. This is basically trying to augment the dataset with all possible permutations of the accelerometer's XYZ axes. This apparently does not work well but it is left there just in case we would need that in the future.



# Real Time Monitoring
