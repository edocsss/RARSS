var sensor = "heartrate";

var SAAgent = null;
var SASocket = null;
var CHANNELID = 104;
var ProviderAppName = "HelloAccessoryProvider";

var MAC = "";

/*
 * SA Functions
 */
var agentCallback = {
		onconnect : function(socket) {
			SASocket = socket;
			console.log("HelloAccessory Connection established with RemotePeer");
			createHTML("startConnection");
			SASocket.setSocketStatusListener(function(reason){
				console.log("Service connection lost, Reason : [" + reason + "]");
				disconnect();
			});
		},
		onerror : onerror
	};


var peerAgentFindCallback = {
	onpeeragentfound : function(peerAgent) {
		try {
			if (peerAgent.appName == ProviderAppName) {
				SAAgent.setServiceConnectionListener(agentCallback);
				SAAgent.requestServiceConnection(peerAgent);
			} else {
				alert("Not expected app!! : " + peerAgent.appName);
			}
		} catch(err) {
			console.log("exception [" + err.name + "] msg[" + err.message + "]");
		}
	},
	onerror : onerror
}

function onsuccess(agents) {
	try {
		if (agents.length > 0) {
			SAAgent = agents[0];
				
			SAAgent.setPeerAgentFindListener(peerAgentFindCallback);
			SAAgent.findPeerAgents();
		} else {
			alert("Not found SAAgent!!");
		}
	} catch(err) {
		console.log("exception [" + err.name + "] msg[" + err.message + "]");
	}
}

function onreceive(channelId, data) 
{
   console.log("Message received - " + channelId + " : " + data); 
}

function connect() {
	if (SASocket) {
		alert('Already connected!');
        return false;
    }
	try {
		webapis.sa.requestSAAgent(onsuccess, function (err) {
			console.log("err [" + err.name + "] msg[" + err.message + "]");
		});
	
	} catch(err) {
		console.log("exception [" + err.name + "] msg[" + err.message + "]");
	}
}

function disconnect() {
	try {
		if (SASocket != null) {
			SASocket.close();
			SASocket = null;
			console.log("closeConnection");
		}
	} catch(err) {
		console.log("exception [" + err.name + "] msg[" + err.message + "]");
	}
}

/*
 * Sensor Collection Functions
 */
var heartrate = new Array();
var interval = 0;
var gettingHeartRate = false;

function checkGettingHeartRate() {
	node = document.getElementById('heartrate_animation');
	
	if (gettingHeartRate) {
		node.style.display = 'inline';
	}
	else {
		node.style.display = 'none';
	}
}

function sensorChange() {
	var sensorCapabilities = webapis.sensorservice.getAvailableSensors();
	for (i = 0; i < sensorCapabilities.length; i++) { 
		console.log("capable sensor : " + sensorCapabilities[i]);
	}
	
	stop();
	document.getElementById("textbox").innerHTML = "";
	var list = document.getElementById("sensor_select");
	sensor = list.options[list.selectedIndex].value;
}

function start() {
	window.tizen.systeminfo.getPropertyValue("WIFI_NETWORK", 
			function(value) {
				MAC = value.macAddress.toLowerCase();
				console.log("MAC: " + MAC);
			}, 
			function(error) {
				console.log("Error getting MAC address");
			});
	//document.getElementById("textbox").innerHTML = sensor;
	tizen.power.request("SCREEN", "SCREEN_NORMAL");

	connect();
	
	if (sensor == "heartrate") {
	    window.webapis.motion.start("HRM", onchangedHeartRate);
	    
	    if (interval <= 0) {
	    	interval = window.setInterval(heartRateInterval, 10000);
	    }
	
	    
	    //document.getElementById("textbox").innerHTML = "Getting heart rate...";
	    
		function onchangedHeartRate(hrmInfo) {
		   if(hrmInfo.heartRate > 0) {
//			   document.getElementById("textbox").innerHTML = hrmInfo.heartRate + " bpm";
		//	   document.getElementById("textbox").innerHTML = hrmInfo.heartRate + " bpm";
			   // var d = new Date();
			  // var dateString = d.getUTCFullYear() + '-' + (d.getUTCMonth() + 1) + '-' + d.getUTCDate() + 'T' + d.getUTCHours() + ':' + d.getUTCMinutes() + ':' + d.getUTCSeconds(); "\"datetime\":" + "\"" + d + "\"," 
			   //SASocket.sendData(CHANNELID, /*hrmInfo.heartRate*/"\"sensor_alias_name\":\"Heartrate 1\",\"data\":" + "\"" + hrmInfo.heartRate + "\"");
			   heartrate.push(hrmInfo.heartRate);
			   gettingHeartRate = false;
		   } else {
			   document.getElementById("textbox").innerHTML = "Measuring...";
			   gettingHeartRate = true;
			   checkGettingHeartRate();
		   }
		}
	}
	
	else if (sensor == "pedometer") {
		
		webapis.motion.setAccumulativePedometerListener(pedometerAccumlator);
		
		document.getElementById("textbox").innerHTML = "Waiting for data...";
		
//		function onchangedPedometer(pedometerInfo) {
//			document.getElementById("textbox").innerHTML = "Total Steps: " + pedometerInfo.cumulativeWalkStepCount + "\nDistance: " + pedometerData.cumulativeDistance;
//			console.log("pedometer callback");
//		}
		
		function pedometerAccumlator(pedometerInfo){
			document.getElementById("textbox").innerHTML = "Total Steps: " + pedometerInfo.accumulativeWalkStepCount + "\nDistance: " + pedometerInfo.accumulativeDistance;
			console.log("pedometer accumlator")
		}
		
	//	 tizen.humanactivitymonitor.start("PEDOMETER", onchangedPedometer);
	//	window.webapis.motion.start("PEDOMETER", onchangedPedometer);
		console.log("pedometer set");
	//	webapis.motion.getMotionInfo("PEDOMETER", onchangedPedometer, error);
	//	document.getElementById("textbox").innerHTML = "Total Steps: " + pedometerInfo.cumulativeWalkStepCount + "\nDistance: " + pedometerData.cumulativeDistance;
	}
	
	else if (sensor == "gps") {
		window.webapis.motion.start("GPS", onchangedGPS);
		
		function onchangedGPS(GPSInfo) {
			document.getElementById("textbox").innerHTML = "Latitude: " + GPSInfo.latitude + "\nLongitude: " + GPSInfo.longitude;
		}
	}
	
	else if (sensor == "ultraviolet") {
		var UVSensor = webapis.sensorservice.getDefaultSensor("ULTRAVIOLET");

		document.getElementById("textbox").innerHTML = "Point sensor towards the sun." ;
		
		function onGetUV(UVInfo) {
			document.getElementById("textbox").innerHTML = "UV Level: " + UVInfo.ultravioletLevel;
	//		SASocket.sendData(CHANNELID, "UV Level: " + UVInfo.ultravioletLevel);
		}
		
		function onchangedUV() {
			UVSensor.getUltravioletSensorData(onGetUV, error);
		}

		UVSensor.start(onchangedUV);
		UVSensor.setChangeListener(onGetUV);
	}
	
	else if (sensor == "light") {
		var lightSensor = webapis.sensorservice.getDefaultSensor("LIGHT");
		
		document.getElementById("textbox").innerHTML = "Point sensor towards the light." ;
		
		function onGetLight(lightInfo) {
			document.getElementById("textbox").innerHTML = "Light Level: " + lightInfo.lightLevel;
	//		SASocket.sendData(CHANNELID, "Light Level: " + lightInfo.lightLevel);
		}
		
		function onchangedLight() {
			lightSensor.getLightSensorData(onGetLight, error);
		}
		
		lightSensor.start(onchangedLight);
		lightSensor.setChangeListener(onGetLight);
	}
	
	else if (sensor == "pressure") {
		var pressureSensor = window.webapis.sensorservice.getDefaultSensor("PRESSURE");
		
		document.getElementById("textbox").innerHTML = "Getting data..." ;
		
		function onGetPressure(pressureInfo) {
			document.getElementById("textbox").innerHTML = "Pressure: " + pressureInfo.pressure;
	//		SASocket.sendData(CHANNELID, "Pressure: " + pressureInfo.pressure);
		}
		
		function onchangedPressure() {
			pressureSensor.getPressureSensorData(onGetPressure, error);
		}
		
		pressureSensor.start(onchangedPressure);
		pressureSensor.setChangeListener(onGetPressure);
	}
	
	else if (sensor == "magnetic") {
		var magneticSensor = webapis.sensorservice.getDefaultSensor("MAGNETIC");
		
		document.getElementById("textbox").innerHTML = "Getting data..." ;
		
		function onGetMagnetic(magneticInfo) {
			document.getElementById("textbox").innerHTML = "x: " + magneticInfo.x + "\n"
														+ "y: " + magneticInfo.y + "\n"
														+ "z: " + magneticInfo.z;
			
			console.log("get magnetic data");
		}
		
		function onchangedMagnetic() {
			//magneticSensor.getMagneticSensorData(onGetMagnetic, error);
			
			console.log("magnetic success");
		}
		
		function magneticError() {
			console.log("magnetic error");
		}
		
		try {
			console.log("set magnetic 1");
			magneticSensor.start(onchangedMagnetic);
			console.log("set magnetic 2");
			magneticSensor.setChangeListener(onGetMagnetic);
			console.log("set magnetic 3");
		}
		catch(error) {
			console.log("magnetic error: " + error.toString());
		}
	}
	
	else if (sensor == "wifi_test") {
		function getWifiStatus(wifiInfo) {
			document.getElementById("textbox").innerHTML = /*"Status: " + wifiInfo.status + "\n"
														+ "SSID: "  + wifiInfo.ssid + "\n"
														+ "Signal Strength: "  + wifiInfo.signalStrength;*/
			"IP Address: " + wifiInfo.ipAddress;
		}
		
		tizen.systeminfo.getPropertyValue("WIFI_NETWORK", getWifiStatus);
		
	}
}

function heartRateInterval() {
	var heartRateToSend = 0;
	for (var i = 0; i < heartrate.length; i++) {
		heartRateToSend += heartrate[i];
	}
	
	// Take the average of all data and send it
	heartRateToSend /= heartrate.length;
	heartRateToSend = Math.floor(heartRateToSend);
	document.getElementById("textbox").innerHTML = heartRateToSend + " bpm";
	checkGettingHeartRate();
	heartrate.length = 0;
	
	SASocket.sendData(CHANNELID, "\"sensor_alias_name\":\"Heartrate 2\",\"data\":\"" + heartRateToSend + "\",\"node_uuid\":\"" + MAC + "\"");
}

function stop() {
	tizen.power.release("SCREEN");
	
	disconnect();
	
	if (sensor == "heartrate") {
		window.clearInterval(interval);
		interval = 0;
		gettingHeartRate = false;
		checkGettingHeartRate();
		document.getElementById("textbox").innerHTML = "Stopped.";
		window.webapis.motion.stop("HRM");
	}
	else if (sensor == "pedometer") {
		document.getElementById("textbox").innerHTML = "Stopped.";
		webapis.motion.unsetAccumulativePedometerListener();
		//window.webapis.motion.stop("PEDOMETER");
		//tizen.humanactivitymonitor.stop("PEDOMETER");
	}
	else if (sensor == "gps") {
		document.getElementById("textbox").innerHTML = "Stopped.";
		window.webapis.motion.stop("GPS");
	}
	
	else if (sensor == "ultraviolet") {
		document.getElementById("textbox").innerHTML = "Stopped.";
		var UVSensor = webapis.sensorservice.getDefaultSensor("ULTRAVIOLET");

		UVSensor.unsetChangeListener();
		UVSensor.stop();
	}
	
	else if (sensor == "light") {
		document.getElementById("textbox").innerHTML = "Stopped.";
		var lightSensor = webapis.sensorservice.getDefaultSensor("LIGHT");

		lightSensor.unsetChangeListener();
		lightSensor.stop();
	}
	
	else if (sensor == "pressure") {
		document.getElementById("textbox").innerHTML = "Stopped.";
		var pressureSensor = webapis.sensorservice.getDefaultSensor("PRESSURE");

		pressureSensor.unsetChangeListener();
		pressureSensor.stop();
	}
	
	else if (sensor == "magnetic") {
		document.getElementById("textbox").innerHTML = "Stopped.";
		var magneticSensor = webapis.sensorservice.getDefaultSensor("MAGNETIC");

		magneticSensor.unsetChangeListener();
		magneticSensor.stop();
	}
}

function error () {
	document.getElementById("textbox").innerHTML = "An error occurred.";
}

function test() {
	document.getElementById("textbox").innerHTML = "this is a test";
}

function openConnection() {
	webSocket.onopen = function(e) 
	{
		console.log('connection open, readyState: ' + e.target.readyState);
	};

	/* If the connection fails or is closed with prejudice */
	webSocket.onerror = function(e) 
	{
		console.log('error, readyState: ' + e.target.readyState);
	};
	
	webSocket.onclose = function(e) 
	{
		console.log('connection close, readyState: ' + e.target.readyState);
	};
	
	webSocket = new WebSocket(webSocketURL);
	
	console.log ("Done connection setup");
}

function closeConnection() 
{
	console.log("Attepting to close connection...");
   if (webSocket.readyState === 1) 
   {
	  console.log("Connection closed");
      webSocket.close();
   }
}

function sendData (data) {
	console.log("Attempting to send data...");
	if (webSocket.readyState === 1) 
	{
		console.log("sending \"" + data + "\"");
		webSocket.send(data);
	}
}

window.onload = function () {
    // add eventListener for tizenhwkey
    document.addEventListener('tizenhwkey', function(e) {
        if(e.keyName == "back")
            tizen.application.getCurrentApplication().exit();
    });
    

};