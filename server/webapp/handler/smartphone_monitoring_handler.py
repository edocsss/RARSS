from tornado.escape import json_decode, json_encode

from util.logger import web_logger as LOGGER
from webapp.handler.base_handler import BaseHandler
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler


class SmartphoneMonitoringHandler(BaseHandler):
    def post(self):
        f = json_decode(self.request.body)
        uuid = f['uuid']
        LOGGER.info('Smartphone: {}'.format(uuid))

        real_time_monitoring_service = self.settings['real_time_monitoring_service']
        real_time_monitoring_service.insert_sp_raw_data_to_db(f)

        SmartwatchWebsocketHandler.broadcast('send_data_monitoring {}'.format(uuid))
        self.write(json_encode({ 'result': True }))