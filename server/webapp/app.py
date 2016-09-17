from flask import Flask, request
from flask_socketio import SocketIO, emit
from webapp.service.sensory_data_service import SensoryDataService
import json


app = Flask(__name__)
socketio = SocketIO(app)
sensory_data_service = SensoryDataService()


@app.route('/', methods=['POST'])
def upload_sensor_data():
    f = request.json
    activity_type = f['activityType']
    file_name = f['fileName']
    file_content = f['fileContent']

    sensory_data_service.store_smartphone_file(activity_type, file_name, file_content)
    return json.dumps({ 'result': True })


@app.route('/smartwatch', methods=['POST'])
def notify_smartwatch():
    d = request.json
    if d['start']:
        print('Smartwatch start!')
    else:
        print('Smartwatch stop!')

    return json.dumps({ 'result': True })


@app.route('/test', methods=['GET'])
def test():
    return json.dumps({ 'result': True })


@socketio.on('connect')
def test_connect():
    print("Smartwatch WS connected!")

@socketio.on('disconnect')
def test_disconnect():
    print("Smartwatch WS disconnected!")


if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0', debug=True)