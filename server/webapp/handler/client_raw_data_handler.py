from tornado.escape import json_decode, json_encode
from webapp.handler.base_handler import BaseHandler
import config as CONFIG


class ClientRawDataHandler(BaseHandler):
    def post(self):
        f = json_decode(self.request.body)
        activity_type = f['activityType']
        data_source = f['dataSource']
        data_subject = f['dataSubject']

        raw_data_service = self.settings['raw_data_service']
        data = raw_data_service.get_raw_data_by_activity_and_source(activity_type, data_source, data_subject)

        if data is None:
            self.write(json_encode({
                'result': False,
                'message': 'Raw data is not available for {} collected from {} by {}!'.format(
                    activity_type,
                    data_source,
                    data_subject
                )
            }))
        else:
            self.write(json_encode({
                'result': True,
                'message': '',
                'data': data
            }))


    def get(self):
        self.write(json_encode({
            'result': True,
            'data': CONFIG.FULL_SUBJECT_LIST
        }))