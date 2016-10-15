var worker = new Worker('worker.js');
worker.onmessage = function (e) {
	console.log(e.data);
};

document.getElementById('stop_button').onclick = function () {
	console.log('Stopping worker...');
	worker.terminate();
};