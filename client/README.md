# FYP Client Web Application
This project is generated with [yo angular generator](https://github.com/yeoman/generator-angular)
version 0.15.1.

# Requirements
1. NPM installed
2. Bower installed
3. Run `npm install` in ```<path_to_client_root_dir>```
4. Run `bower install` in ```<path_to_client_root_dir>```

# Build & Development
Run `grunt` for building and `grunt serve` for preview from ```<path_to_client_root_dir>```.
Running `grunt serve` will open the website in a new tab in your default browser.

# Using the Data Explorer
This client AngularJS web application is able to generate charts based on the raw data stored in the server. You can easily choose the type of activities, the subject name, and the data source (Smartphone or Smartwatch).

# Preparing Real Time Monitoring
1. Run the `Tornado` server and configure the `Server URL` for the Smartphone and Smartwatch application.
   - If you are not using `ngrok` as the tunneling provider, you need to dive into the Smartphone and Smartwatch code to change your preferred way of updating the URL!
   
2. Run the MongoDB server
   - The script ```<path_to_server_root_dir>/run_mongod.sh``` can be used to run the MongoDB server with the configuration found in ```<path_to_server_root_dir>/mongod.cfg```.
   - Make sure to run the ```run_mongod.sh``` script from ```bash``` terminal (or create your own `.bat` script) and make sure the current working directory is the ```<path_to_server_root_dir>``` since the configuration is using **relative path**!
   
3. Open the `Real Time Monitoring` activity in the Smartphone application.
4. Open the Smartwatch application.
   - Make sure the WebSocket is connected
5. Open the web application in your browser (**do not forget to run the web server!**) and go to the root page.
6. Press on the `Start Monitoring` button in the Smartphone application.
7. This will trigger the Smartwatch to start recording.
8. The server will then take care of the data reading from MongoDB, preprocessing the data, and send the predicted activity to the AngularJS web application.

# Training the Real Time Model
The model training is in the `server/classifier/real_time_monitoring` folder. Please be sure the configuration used and which dataset to use for training. Once the model is ready, then you can try the real time monitoring

# Real Time Monitoring Logic
Please take a look at the `server` folder `README` file.
