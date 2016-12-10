from io import StringIO

import pandas as pd

from webapp.db.raw_sensory_data_db import RawSensoryDataDb
from webapp.db.work_queue_db import WorkQueueDb
from webapp.util import smartwatch_data_converter


class RealTimeMonitoringService():
    def __init__(self):
        self._raw_data_db = RawSensoryDataDb()
        self._work_queue_db = WorkQueueDb()


    def insert_sp_raw_data_to_db(self, json_data):
        uuid = json_data['uuid']
        sp_accelerometer_data = self._convert_sensory_json_data_to_db_format(json_data['sp_accelerometer'])
        self._raw_data_db.insert_sp_raw_accelerometer_data(uuid, sp_accelerometer_data)


    def insert_sw_raw_data_to_db(self, json_data):
        uuid = json_data['uuid']
        sw_accelerometer_data = self._convert_smartwatch_data_to_common_format(json_data)
        sw_accelerometer_data = self._convert_sensory_json_data_to_db_format(sw_accelerometer_data['sw_accelerometer'])

        self._raw_data_db.insert_sw_raw_accelerometer_data(uuid, sw_accelerometer_data)
        self._work_queue_db.insert_uuid(uuid)


    def _convert_sensory_json_data_to_db_format(self, sensory_data):
        df = pd.read_csv(StringIO(sensory_data), sep=',')
        cols = df.columns

        return [{
            col: item[col] for col in cols
        } for i, item in df.iterrows()]


    def _convert_smartwatch_data_to_common_format(self, sw_data):
        accelerometer_data = sw_data['sw_accelerometer']
        sw_data['sw_accelerometer'] = smartwatch_data_converter.convert_smartwatch_accelerometer_data_to_csv(accelerometer_data)
        return sw_data


if __name__ == '__main__':
    r = RealTimeMonitoringService()
    r.insert_sp_raw_data_to_db({
        'uuid': '18',
        'sp_accelerometer': 'timestamp,ax,ay,az\n124,2.000,-1.000,0.000\n'
    })

    r.insert_sw_raw_data_to_db({
        'uuid': '18',
        'sw_accelerometer': [{
            'timestamp': 1000,
            'ax': 1.0,
            'ay': 2.0,
            'az': 3.0
        }]
    })