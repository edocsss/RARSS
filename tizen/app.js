(function () {
	var SENSOR_INTERVAL = 200; // in ms
	var SERVER_URL = 'http://788d9f3a.ngrok.io';
	var DATA_UPLOAD_URL = SERVER_URL + '/smartwatch/upload';
	var WEBSOCKET_URL = 'ws://788d9f3a.ngrok.io/smartwatch/ws';
	
	var ACCELEROMETER_LOCALSTORAGE_KEY = 'accelerometer';
	var GYROSCOPE_LOCALSTORAGE_KEY = 'gyroscope';
	var LIGHT_LOCALSTORAGE_KEY = 'light';
	var PRESSURE_LOCALSTORAGE_KEY = 'pressure';
	var MAGNETIC_LOCALSTORAGE_KEY = 'magnetic';
	var ULTRAVIOLET_LOCALSTORAGE_KEY = 'ultraviolet';
	
	var activityType = '';
	var startRecording = false;
	var sensorReadings = {
			accelerometer: { data: [] },
			gyroscope: { data: [] },
			light: { data: [] },
			pressure: { data: [] },
			magnetic: { date: 0, data: [] },
			uv: { date: 0, data: [] }
	};
	
	var lightSensor;
	var magneticSensor;
	var pressureSensor;
	var uvSensor;
	
	var socket;
	setupWebsocket();
	
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
		sendSensoryDataToServer();
	};
	
	document.getElementById('setup_websocket_data').onclick = function () {
		setupWebsocket();
	};
	
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
		
		setupLightSensor();
		setupMagneticSensor();
		setupPressureSensor();
		setupUVSensor();
		
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
	
	function sendSensoryDataToServer(fileId) {
		var sensorData = loadSensoryDataFromLocalStorage();
		sendData({
			activityType: activityType,
			sensoryData: sensorData,
			fileId: fileId
		});
	}
	
	function sendData(data) {
		console.log("Sending data to server..");
		var xhr = new XMLHttpRequest();
		xhr.open('POST', DATA_UPLOAD_URL);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.onerror = function () {
			console.log('XHR ERror!');
		};
		
		xhr.send(JSON.stringify(data));
		console.log("Data sent to server!");
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
				setupAllSensors();
			} else if (message === 'stop_recording') {
				stopAndUnsetAllSensors();
			} else if (message.indexOf('send_data') > -1) {
				var fileId = message.split(' ')[1];
				sendSensoryDataToServer(fileId);
			}
		};
	}
	
	function getCurrentTimestamp() {
		return new Date().getTime();
	}
}());