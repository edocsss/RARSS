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
1. Run the MongoDB server
2. Simply run ```<path_to_server_root_dir>/webapp/tornado.py``` from the IDE
3. This will run the Web Server at the port specified in ```<path_to_server_root_dir>/webapp/web_config.py```



# Smartphone and Smarwatch Synchronization during Activity Recording
One issue with using Tizen Smartwatch is that the documention is not very good and hence I chose not to pair the Smartwatch and Smartphone via Bluetooth connection. In this project, I decided to use WebSocket to perform push notification from the server to the Smartwatch.

This section here will briefly discuss how the Smartphone and Smartwatch interact with each other so that when the activity recording is stopped, both devices can send the raw sensory data to the server correctly.

### Start Activity Recording
1. When the ```Start Recording``` button found in the Smartphone application, the Smartphone will send an HTTP request to the server and the server will notify the Smartwatch with sufficient information about the activity. The information sent is only the ```activity type``` being recorded.
2. The Smartphone will start recording the sensor readings.
3. The Smartwatch will receive this information via WebSocket, store the ```activity type``` locally, and start recording the sensor readings.

**PLEASE NOTE THAT THERE IS NO DELAY BETWEEN PRESSING THE START RECORDING BUTTON AND THE SENSOR READINGS RECORDING!!**

### Stop Activity Recording
1. When the ```Stop Recording``` button found in the Smartphone application OR the timer has ended, the Smartphone will stop recording the sensor readings immediately.
2. The Smartphone will bundle all the readings and send it to the server via HTTP.
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

In order to generate the combined and pre-processed data, the only thing you need to do is run the ```<path_to_server_root_dir>/data_processor/data_preprocessor.py```. This will take quite some time depending on how many activities you would like to pre-process and the configurations used. You can also specify the activities you would like to pre-process in the same Python file.

### Configuration
Please change the data pre-processing configurations in ```<path_to_server_root_dir>/config.py``` accordignly!

### Features
At the moment, we are only using the ```Accelerometer``` data from both Smartphone and Smartwatch. The features generated for the Smartphone and Smartwatch are the same. The features considered are:
1. Mean
2. Variance
3. Covariance (all combinations between x-axis, y-axis, z-axis, and magnitude)
4. Energy
5. Entropy

For features other than the ```covariance```, they are applied to all 3-axes (x, y, and z) and the accelerometer magnitude (calculated in the server using the usual vector magnitude formula). In addition, the formula used for the ```Energy``` and ```Entropy``` can be found in Prof. Tan's and Dr. Wang's paper: **Non Intrusive Robust Human Activity Recognition for Diverse Age Groups**.



# Model K-Fold Cross Validation
All K-Fold CV related files can be found in ```<path_to_server_root_dir>/classifier/cv```.

### Data Pre-processing for Models
After features are generated and before building the model, there are some additional data pre-processings required.
1. Encoding the activity type with an integer
2. Normalizing each feature into [0, 1] range
3. **[Only for MLP]** Encoding the activity type using onehot method

### Model Configuration
Each model Python file will have a `__main__` part in which you can change the parameters related to each model. If you would like to change more general configurations like the `training size`, `testing size`, or `whose data to use for training and/or testing`, you can change those in ```<path_to_server_root_dir>/config.py```.

### Model Validation
There are 4 models we are currently using: SVM, Random Forest, Naive Bayes, and Multi-Layer Perceptron (MLP). MLP training will take quite some time to finish while the other 3 models will finish almost instantly for the same amount of data.

Model Validation using the K-Fold CV can be easily done by running the corresponding Python file. For example, if you would like to test SVM model, run  ```<path_to_server_root_dir>/classifier/cv/svm.py```.