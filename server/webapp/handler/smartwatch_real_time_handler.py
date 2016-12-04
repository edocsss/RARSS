from tornado.escape import json_decode, json_encode
from webapp.handler.base_handler import BaseHandler
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler
from webapp.util.logger import web_logger as LOGGER


class SmartwatchRealTimeHandler(BaseHandler):
    def post(self):
        raw_data_service = self.settings['raw_data_service']