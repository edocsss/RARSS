from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode
from webapp.service.sensory_data_service import SensoryDataService

sensory_data_service = SensoryDataService()
class SmartphoneHandler(RequestHandler):
    def post(self):
        print(self.request.body)
        f = json_decode(self.request.body)
        activity_type = f['activityType']
        file_name = f['fileName']
        file_content = f['fileContent']

        sensory_data_service.store_smartphone_file(activity_type, file_name, file_content)
        self.write(json_encode({'result': True}))

    def get(self):
        print("TEST")
        self.write(json_encode({'result': True}))