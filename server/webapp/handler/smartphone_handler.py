from tornado.escape import json_decode, json_encode
from webapp.handler.base_handler import BaseHandler
from webapp.service.sensory_data_service import SensoryDataService
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler
import time


sensory_data_service = SensoryDataService()


class SmartphoneHandler(BaseHandler):
    def post(self):
        print(self.request.body)
        f = json_decode(self.request.body)

        activity_type = f['activityType']
        sensory_data = f['sensoryData']
        file_id = str(f['fileId'])

        sensory_data_service.handle_smartphone_sensory_data(activity_type, sensory_data, file_id)
        SmartwatchWebsocketHandler.broadcast('send_data {}'.format(file_id))
        self.write(json_encode({'result': True}))


    def get(self):
        print("TEST")
        self.write(json_encode({'result': True}))