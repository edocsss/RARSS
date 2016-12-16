from tornado.escape import json_decode, json_encode

from util.logger import web_logger as LOGGER
from webapp.handler.base_handler import BaseHandler


"""
Handles the raw data sent from the Smartwatch application for the Real Time Monitoring flow.
"""


class SmartwatchMonitoringHandler(BaseHandler):
    def post(self):
        f = json_decode(self.request.body)
        LOGGER.info('SMARTWATCH MONITORING DATA RECEIVED!')
        real_time_monitoring_service = self.settings['real_time_monitoring_service']

        real_time_monitoring_service.insert_sw_raw_data_to_db(f)
        self.write(json_encode({'result': True}))