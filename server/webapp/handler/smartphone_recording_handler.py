from tornado.escape import json_decode, json_encode

from util.logger import web_logger as LOGGER
from webapp.handler.base_handler import BaseHandler
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler


"""
Handles the raw data sent from the Smartphone application for the Activity Recording.
"""


class SmartphoneRecordingHandler(BaseHandler):
    def post(self):
        f = json_decode(self.request.body)
        activity_type = f['activityType']
        sensory_data = f['sensoryData']
        file_id = str(f['fileId'])
        LOGGER.info('Smartphone: {}'.format(file_id))

        sensory_data_service = self.settings['sensory_data_service']
        sensory_data_service.handle_smartphone_sensory_data(activity_type, sensory_data, file_id)

        SmartwatchWebsocketHandler.broadcast('send_data_recording {}'.format(file_id))
        self.write(json_encode({'result': True}))