from tornado.escape import json_decode, json_encode

from util.logger import web_logger as LOGGER
from webapp.handler.base_handler import BaseHandler


class SmartwatchRecordingHandler(BaseHandler):
    def post(self):
        d = json_decode(self.request.body)
        activity_type = d['activityType']
        sensory_data = d['sensoryData']
        file_id = str(d['fileId'])
        LOGGER.info("Smartwatch: {}".format(file_id))

        sensory_data_service = self.settings['sensory_data_service']
        sensory_data_service.handle_smartwatch_sensory_data(activity_type, sensory_data, file_id)
        # data_preprocessor.preprocess_data(activity_type) # Data processing is only done when both Smartphone and Smartwatch data is stored
        self.write(json_encode({'result': True}))