from tornado.escape import json_decode, json_encode
from webapp.handler.base_handler import BaseHandler
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler
from webapp.util.logger import web_logger as LOGGER


class SmartphoneRealTimeHandler(BaseHandler):
    def post(self):
        f = json_decode(self.request.body)
        sensory_data = f['sensoryData']

        raw_data_service = self.settings['raw_data_service']