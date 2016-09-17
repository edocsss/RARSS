from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler

class SmartwatchNotifierHandler(RequestHandler):
    def post(self):
        d = json_decode(self.request.body)
        if d['start']:
            print('Smartwatch start!')
            SmartwatchWebsocketHandler.broadcast('start_recording {}'.format(d['activityType']))

        else:
            print('Smartwatch stop!')
            SmartwatchWebsocketHandler.broadcast('stop_recording')

        self.write(json_encode({'result': True}))