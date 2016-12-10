from tornado.escape import json_decode, json_encode
from tornado.web import RequestHandler

from util.logger import web_logger as LOGGER
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler


class SmartwatchRecordingNotifierHandler(RequestHandler):
    def post(self):
        d = json_decode(self.request.body)
        if d['start']:
            LOGGER.info('Smartwatch recording start!')
            SmartwatchWebsocketHandler.broadcast('start_recording {}'.format(d['activityType']))

        else:
            LOGGER.info('Smartwatch recording stop!')
            SmartwatchWebsocketHandler.broadcast('stop_recording')

        self.write(json_encode({'result': True}))