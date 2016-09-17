from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode
from webapp.service.sensory_data_service import SensoryDataService

sensory_data_service = SensoryDataService()
class SmartwatchHandler(RequestHandler):
    def post(self):
        d = json_decode(self.request.body)
        print(d)

        file_date = d['fileDate']
        sensor_type = d['sensorType']
        activity_type = d['activityType']
        file_name = d['fileName']
        file_content = d['fileContent']

        if sensor_type == 'accelerometer':
            file_content = sensory_data_service.convert_smartwatch_accelerometer_data_to_csv(file_content)
        elif sensor_type == 'gyroscope':
            file_content = sensory_data_service.convert_smartwatch_gyroscope_data_to_csv(file_content)
        elif sensor_type == 'light':
            file_content = sensory_data_service.convert_smartwatch_light_data_to_csv(file_content)
        elif sensor_type == 'pressure':
            file_content = sensory_data_service.convert_smartwatch_pressure_data_to_csv(file_content)
        elif sensor_type == 'magnetic':
            file_content = sensory_data_service.convert_smartwatch_magnetic_data_to_csv(file_content)
        elif sensor_type == 'ultraviolet':
            file_content = sensory_data_service.convert_smartwatch_ultraviolet_data_to_csv(file_content)

        sensory_data_service.store_smartwatch_file(activity_type, file_name, file_content, file_date)
        self.write(json_encode({'result': True}))