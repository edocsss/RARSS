from tornado.escape import json_decode, json_encode
from webapp.handler.base_handler import BaseHandler
from webapp.service.raw_data_service import RawDataService


raw_data_service = RawDataService()


class ClientRawDataHandler(BaseHandler):
    def post(self):
        f = json_decode(self.request.body)
        activity_type = f['activityType']
        data_source = f['dataSource']

        data = raw_data_service.get_raw_data_by_activity_and_source(activity_type, data_source)
        if data is None:
            self.write(json_encode({
                'result': False,
                'message': 'Raw data is not available for {} from {}!'.format(
                    activity_type,
                    data_source
                )
            }))

        else:
            self.write(json_encode({
                'result': True,
                'message': '',
                'data': data
            }))