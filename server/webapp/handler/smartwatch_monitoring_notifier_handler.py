from tornado.escape import json_decode, json_encode
from tornado.web import RequestHandler

from util.logger import web_logger as LOGGER
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler


"""
Handles HTTP request from Smartphone for notifying the Smartwatch to either start or stop the Real Time Monitoring.
"""


class SmartwatchMonitoringNotifierHandler(RequestHandler):
    def post(self):
        d = json_decode(self.request.body)
        if d['start']:
            LOGGER.info('Smartwatch monitoring start!')
            SmartwatchWebsocketHandler.broadcast('start_monitoring')

        else:
            LOGGER.info('Smartwatch monitoring stop!')
            SmartwatchWebsocketHandler.broadcast('stop_monitoring')

        self.write(json_encode({'result': True}))