(function () {
	var SENSOR_INTERVAL = 200; // in ms
	var SERVER_URL = 'http://01441106.ngrok.io';
	var DATA_RECORDING_UPLOAD_URL = SERVER_URL + '/smartwatch/recording';
	var DATA_MONITORING_UPLOAD_URL = SERVER_URL + '/smartwatch/monitoring';
	var WEBSOCKET_URL = 'ws://01441106.ngrok.io/smartwatch/ws';
	
	var ACCELEROMETER_LOCALSTORAGE_KEY = 'accelerometer';
	var GYROSCOPE_LOCALSTORAGE_KEY = 'gyroscope';
	var LIGHT_LOCALSTORAGE_KEY = 'light';
	var PRESSURE_LOCALSTORAGE_KEY = 'pressure';
	var MAGNETIC_LOCALSTORAGE_KEY = 'magnetic';
	var ULTRAVIOLET_LOCALSTORAGE_KEY = 'ultraviolet';
	var SERVER_URL_KEY = 'tunnelId';
	
	var activityType = '';
	var startRecording = false;
	var realTime = false;
	var sensorReadings = {
		accelerometer: { data: [] },
		gyroscope: { data: [] },
		light: { data: [] },
		pressure: { data: [] },
		magnetic: { data: [] },
		uv: { data: [] }
	};
	
	var lightSensor;
	var magneticSensor;
	var pressureSensor;
	var uvSensor;
	
	var socket;
	
	setupWebsocket();
	loadServerURLPreferences();
	
	window.addEventListener( 'tizenhwkey', function( ev ) {
		if (ev.keyName === "back") {
			var page = document.getElementsByClassName('ui-page-active')[0],
				pageid = page ? page.id : "";
			
			if (pageid === "main") {
				try {
					tizen.application.getCurrentApplication().exit();
				} catch (ignore) {
				}
			} else {
				window.history.back();
			}
		}
	});
	
	var prevTimestamp = getCurrentTimestamp();
	window.addEventListener('devicemotion', function (e) {
		if (getCurrentTimestamp() - prevTimestamp >= SENSOR_INTERVAL) {
			var ax = e.accelerationIncludingGravity.x;
			var ay = -e.accelerationIncludingGravity.y;
			var az = -e.accelerationIncludingGravity.z;
			
			var gx = e.rotationRate.alpha;
			var gy = e.rotationRate.beta;
			var gz = e.rotationRate.gamma;
			
			document.getElementById("accelerometer_x").innerHTML = 'AX: ' + ax;
			document.getElementById("accelerometer_y").innerHTML = 'AY: ' + ay;
			document.getElementById("accelerometer_z").innerHTML = 'AZ: ' + az;
			
			document.getElementById("rotation_x").innerHTML = 'GX: ' + gx;
			document.getElementById("rotation_y").innerHTML = 'GY: ' + gy;
			document.getElementById("rotation_z").innerHTML = 'GZ: ' + gz;
			
			if (startRecording) {
				sensorReadings.accelerometer.data.push({ ax: ax, ay: ay, az: az, timestamp: getCurrentTimestamp() });
				sensorReadings.gyroscope.data.push({ gx: gx, gy: gy, gz: gz, timestamp: getCurrentTimestamp() });
			}
			
			prevTimestamp = getCurrentTimestamp();
		}
	});
	
	document.getElementById('start_button').onclick = function () {
		setupAllSensors();
	};
	
	document.getElementById('stop_button').onclick = function () {
		stopAndUnsetAllSensors();
	};
	
	document.getElementById('send_data_button').onclick = function () {
		sendSensoryDataRecordingToServer();
	};
	
	document.getElementById('setup_websocket_data').onclick = function () {
		socket.onclose = function () {};
		socket.close();
		setupWebsocket();
	};
	
	document.getElementById('save_url_button').onclick = function () {
		var tunnelId = document.getElementById('url_textbox').value;
		localStorage.setItem(SERVER_URL_KEY, tunnelId);
		setupServerURL(tunnelId);
		console.log(tunnelId);
	};
	
	function loadServerURLPreferences() {
		var tunnelId = localStorage.getItem(SERVER_URL_KEY);
		if (!!tunnelId) {
			setupServerURL(tunnelId);
			document.getElementById('url_textbox').value = tunnelId;
		}
	}
	
	function setupServerURL(tunnelId) {
		SERVER_URL = 'http://' + tunnelId + '.ngrok.io';
		DATA_RECORDING_UPLOAD_URL = SERVER_URL + '/smartwatch/recording';
		DATA_MONITORING_UPLOAD_URL = SERVER_URL + '/smartwatch/monitoring';
		WEBSOCKET_URL = 'ws://' + tunnelId + '.ngrok.io/smartwatch/ws';
	}
	
	function setupLightSensor() {
		var prevLightReading = getCurrentTimestamp();
		lightSensor =  webapis.sensorservice.getDefaultSensor('LIGHT');
		
		lightSensor.setChangeListener(function (data) {
			if (getCurrentTimestamp() - prevLightReading >= SENSOR_INTERVAL) {
				document.getElementById('light').innerHTML = 'Light: ' + data.lightLevel;
				if (startRecording) {
					sensorReadings.light.data.push({ light: data.lightLevel, timestamp: getCurrentTimestamp() });
				}
				
				prevLightReading = getCurrentTimestamp();
			}
		});
		
		lightSensor.start(function () {
			console.log('Light sensor started!');
		});
	}
	
	function setupMagneticSensor() {
		var prevMagneticReading = getCurrentTimestamp();
		magneticSensor = webapis.sensorservice.getDefaultSensor('MAGNETIC');
		
		magneticSensor.setChangeListener(function (data) {
			if (getCurrentTimestamp() - prevMagneticReading >= SENSOR_INTERVAL) {
				document.getElementById('magnetic_x').innerHTML = 'MX: ' + data.x;
				document.getElementById('magnetic_y').innerHTML = 'MY: ' + data.y;
				document.getElementById('magnetic_z').innerHTML = 'MZ: ' + data.z;
				document.getElementById('magnetic_accuracy').innerHTML = 'Acc: ' + data.accuracy;
				
				if (startRecording) { 
					sensorReadings.magnetic.data.push({ mx: data.x, my: data.y, mz: data.z, mAcc: data.accuracy, timestamp: getCurrentTimestamp() });
				}
				
				prevMagneticReading = getCurrentTimestamp();
			}
		});
		
		magneticSensor.start(function () {
			console.log("Magnetic sensor started!");
		});
	}
	
	function setupPressureSensor() {
		var prevPressureReading = getCurrentTimestamp();
		pressureSensor = webapis.sensorservice.getDefaultSensor('PRESSURE');
		
		pressureSensor.setChangeListener(function (data) {
			if (getCurrentTimestamp() - prevPressureReading >= SENSOR_INTERVAL) {
				document.getElementById('pressure').innerHTML = 'Pres: ' + data.pressure;
				if (startRecording) {
					sensorReadings.pressure.data.push({ pressure: data.pressure, timestamp: getCurrentTimestamp() });
				}
				
				prevPressureReading = getCurrentTimestamp();
			}
		});
		
		pressureSensor.start(function () {
			console.log("Pressure sensor started!");
		});
	}
	
	function setupUVSensor() {
		var prevUVReading = getCurrentTimestamp();
		uvSensor = webapis.sensorservice.getDefaultSensor('ULTRAVIOLET');
		uvSensor.setChangeListener(function (data) {
			if (getCurrentTimestamp() - prevUVReading >= SENSOR_INTERVAL) {
				document.getElementById('ultraviolet').innerHTML = 'UV: ' + data.ultravioletLevel;
				if (startRecording) {
					sensorReadings.uv.data.push({ uv: data.ultravioletLevel, timestamp: getCurrentTimestamp() });
				}
				
				prevUVReading = getCurrentTimestamp();
			}
		});
		
		uvSensor.start(function () {
			console.log("UV sensor started!");
		});
	}
	
	function setupAllSensors() {
		console.log('Starting all sensors!');
		startRecording = true;
		
		if (!realTime) {
			setupLightSensor();
			setupMagneticSensor();
			setupUVSensor();
		} else {
			setupPressureSensor();
		}
		
		tizen.power.request("SCREEN", "SCREEN_NORMAL");
		tizen.power.request("CPU", "CPU_AWAKE");
	}
	
	function stopAndUnsetAllSensors() {
		console.log('Stopping all sensors!');
		startRecording = false;
		
		lightSensor.unsetChangeListener();
		lightSensor.stop();
		
		magneticSensor.unsetChangeListener();
		magneticSensor.stop();
		
		pressureSensor.unsetChangeListener();
		pressureSensor.stop();
		
		uvSensor.unsetChangeListener();
		uvSensor.stop();
		
		storeSensoryDataToLocalStorage();
		tizen.power.release("SCREEN");
		tizen.power.release("CPU");
	}
	
	function storeSensoryDataToLocalStorage() {
		console.log('Storing data to local storage...');		
		localStorage.setItem(ACCELEROMETER_LOCALSTORAGE_KEY, JSON.stringify(sensorReadings.accelerometer));
		localStorage.setItem(GYROSCOPE_LOCALSTORAGE_KEY, JSON.stringify(sensorReadings.gyroscope));
		localStorage.setItem(LIGHT_LOCALSTORAGE_KEY, JSON.stringify(sensorReadings.light));
		localStorage.setItem(PRESSURE_LOCALSTORAGE_KEY, JSON.stringify(sensorReadings.pressure));
		localStorage.setItem(MAGNETIC_LOCALSTORAGE_KEY, JSON.stringify(sensorReadings.magnetic));
		localStorage.setItem(ULTRAVIOLET_LOCALSTORAGE_KEY, JSON.stringify(sensorReadings.uv));
	}
	
	function loadSensoryDataFromLocalStorage() {
		console.log('Loading data from local storage...');
		var data = {
			accelerometer: JSON.parse(localStorage.getItem(ACCELEROMETER_LOCALSTORAGE_KEY)),
			gyroscope: JSON.parse(localStorage.getItem(GYROSCOPE_LOCALSTORAGE_KEY)),
			light: JSON.parse(localStorage.getItem(LIGHT_LOCALSTORAGE_KEY)),
			pressure: JSON.parse(localStorage.getItem(PRESSURE_LOCALSTORAGE_KEY)),
			magnetic: JSON.parse(localStorage.getItem(MAGNETIC_LOCALSTORAGE_KEY)),
			uv: JSON.parse(localStorage.getItem(ULTRAVIOLET_LOCALSTORAGE_KEY))
		};
		
		console.log('Data loaded!');
		return data;
	}
	
	function sendSensoryDataRecordingToServer(fileId) {
		var sensorData = loadSensoryDataFromLocalStorage();
		sendDataForActivityRecording({
			activityType: activityType,
			sensoryData: sensorData,
			fileId: fileId
		});
	}
	
	function sendSensoryDataMonitoringToServer(uuid) {
		var data = { uuid: uuid };
		for (var key in sensorReadings) {
			data['sw_' + key] = sensorReadings[key].data;
			sensorReadings[key].data = [];
		}
		
		sendDataForMonitoring(data);
	}
	
	function sendData(url, data) {
		console.log("Sending data to server..");
		var xhr = new XMLHttpRequest();
		xhr.open('POST', url);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.onerror = function () {
			console.log('XHR Error!');
		};
		
		xhr.send(JSON.stringify(data));
		console.log("Data sent to server!");
	}
	
	function sendDataForActivityRecording(data) {
		sendData(DATA_RECORDING_UPLOAD_URL, data);
	}
	
	function sendDataForMonitoring(data) {
		sendData(DATA_MONITORING_UPLOAD_URL, data);
	}
	
	var MAX_WS_RETRY = 10;
	var retryCounter = 0;
	
	function setupWebsocket() {		
		socket = new WebSocket(WEBSOCKET_URL);
		socket.onopen = function (e) {
			console.log('WebSocket connection open, ready state: ' + e.target.readyState);
		};
		
		socket.onerror = function (e) {
			console.log(e);
			console.log('WebSocket error! ready state: ' + e.target.readyState);
		};
		
		socket.onclose = function (e) {
			console.log('WebSocket connection close, ready state: ' + e.target.readyState);
			if (retryCounter < MAX_WS_RETRY) {
				setTimeout(function () {
					setupWebsocket();
				}, 1000);
			} else {
				retryCounter = 0;
				return;
			}
			
			retryCounter++;
		};
		
		socket.onmessage = function (e) {
			var message = e.data;
			if (message.indexOf('start_recording') > -1) {
				activityType = message.split(' ')[1];
				realTime = false;
				setupAllSensors();
			} else if (message === 'stop_recording') {
				stopAndUnsetAllSensors();
			} else if (message.indexOf('send_data_recording') > -1) {
				var fileId = message.split(' ')[1];
				sendSensoryDataRecordingToServer(fileId);
			} else if (message.indexOf('start_monitoring') > -1) {
				sensorReadings = {
					accelerometer: { data: [] },
					gyroscope: { data: [] },
					light: { data: [] },
					pressure: { data: [] },
					magnetic: { data: [] },
					uv: { data: [] }
				};
				
				console.log('START_MONITORING');
				realTime = true;
				setupAllSensors();
			} else if (message.indexOf('stop_monitoring') > -1) {
				console.log('STOP_MONITORING');
				stopAndUnsetAllSensors();
			} else if (message.indexOf('send_data_monitoring') > -1) {
				console.log('SEND_DATA_MONITORING');
				var uuid = message.split(' ')[1];
				sendSensoryDataMonitoringToServer(uuid);
			}
		};
	}
	
	function getCurrentTimestamp() {
		return new Date().getTime();
	}
}());