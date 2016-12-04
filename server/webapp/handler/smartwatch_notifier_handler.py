from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler
from webapp.util.logger import web_logger as LOGGER


class SmartwatchNotifierHandler(RequestHandler):
    def post(self):
        d = json_decode(self.request.body)
        if d['start']:
            LOGGER.info('Smartwatch start!')
            SmartwatchWebsocketHandler.broadcast('start_recording {}'.format(d['activityType']))

        else:
            LOGGER.info('Smartwatch stop!')
            SmartwatchWebsocketHandler.broadcast('stop_recording')

        self.write(json_encode({'result': True}))