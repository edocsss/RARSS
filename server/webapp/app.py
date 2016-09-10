from flask import Flask, request
from webapp.service.sensory_data_service import SensoryDataService
import json

app = Flask(__name__)
sensory_data_service = SensoryDataService()

@app.route('/', methods=['POST'])
def upload_sensor_data():
    f = request.json
    activity_type = f['activityType']
    file_name = f['fileName']
    file_content = f['fileContent']

    sensory_data_service.store_file(activity_type, file_name, file_content)
    return json.dumps({ 'result': True })

@app.route('/test', methods=['GET'])
def test():
    return 'Test'

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, threaded=True)