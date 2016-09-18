from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode
from webapp.service.sensory_data_service import SensoryDataService
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler


sensory_data_service = SensoryDataService()
class SmartphoneHandler(RequestHandler):
    def post(self):
        print(self.request.body)
        f = json_decode(self.request.body)

        activity_type = f['activityType']
        sensory_data = f['sensoryData']

        sensory_data_service.handle_smartphone_sensory_data(activity_type, sensory_data)
        SmartwatchWebsocketHandler.broadcast('send data')
        self.write(json_encode({'result': True}))

    def get(self):
        print("TEST")
        self.write(json_encode({'result': True}))