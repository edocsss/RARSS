(function () {
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
	
	window.addEventListener('devicemotion', function (e) {
		var ax = e.accelerationIncludingGravity.x;
		var ay = -e.accelerationIncludingGravity.y;
		var az = -e.accelerationIncludingGravity.z;
		
		var rx = e.rotationRate.alpha;
		var ry = e.rotationRate.beta;
		var rz = e.rotationRate.gamma;
		
		document.getElementById("accelerometer_x").innerHTML = 'AX: ' + ax;
		document.getElementById("accelerometer_y").innerHTML = 'AY: ' + ay;
		document.getElementById("accelerometer_z").innerHTML = 'AZ: ' + az;
		
		document.getElementById("rotation_x").innerHTML = 'RX: ' + rx;
		document.getElementById("rotation_y").innerHTML = 'RY: ' + ry;
		document.getElementById("rotation_z").innerHTML = 'RZ: ' + rz;
	});
	
	function getCurrentTimestamp() {
		return new Date().getTime();
	}
}());
