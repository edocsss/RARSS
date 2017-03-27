from io import StringIO

import pandas as pd

from webapp.db.raw_sensory_data_db import RawSensoryDataDb
from webapp.db.work_queue_db import WorkQueueDb
from webapp.util import smartwatch_data_converter


"""
Provides services related to the Real Time Monitoring flow as needed by the Smartphone and Smartwatch.
Mostly it is related to inserting raw data sent from the Smartphone and Smartwatch to the correct MongoDB collections.
"""


class RealTimeMonitoringService():
    def __init__(self):
        self._raw_data_db = RawSensoryDataDb()
        self._work_queue_db = WorkQueueDb()

    def insert_sp_raw_data_to_db(self, json_data):
        uuid = json_data['uuid']
        sp_accelerometer_data = self._convert_sensory_csv_format_to_db_format(json_data['sp_accelerometer'])
        sp_gyroscope_data = self._convert_sensory_csv_format_to_db_format(json_data['sp_gyroscope'])
        sp_barometer_data = self._convert_sensory_csv_format_to_db_format(json_data['sp_barometer'])

        self._raw_data_db.insert_sp_raw_accelerometer_data(uuid, sp_accelerometer_data)
        self._raw_data_db.insert_sp_raw_gyroscope_data(uuid, sp_gyroscope_data)
        self._raw_data_db.insert_sp_raw_barometer_data(uuid, sp_barometer_data)

    def insert_sw_raw_data_to_db(self, json_data):
        uuid = json_data['uuid']
        json_data = self._convert_smartwatch_data_to_csv_format(json_data)

        sw_accelerometer_data = self._convert_sensory_csv_format_to_db_format(json_data['sw_accelerometer'])
        sw_gyroscope_data = self._convert_sensory_csv_format_to_db_format(json_data['sw_gyroscope'])
        sw_barometer_data = self._convert_sensory_csv_format_to_db_format(json_data['sw_barometer'])

        self._raw_data_db.insert_sw_raw_accelerometer_data(uuid, sw_accelerometer_data)
        self._raw_data_db.insert_sw_raw_gyroscope_data(uuid, sw_gyroscope_data)
        self._raw_data_db.insert_sw_raw_barometer_data(uuid, sw_barometer_data)
        self._work_queue_db.insert_uuid(uuid)

    # Convert raw data in CSV format to the MongoDB dictionary format
    def _convert_sensory_csv_format_to_db_format(self, sensory_data_csv):
        df = pd.read_csv(StringIO(sensory_data_csv), sep=',')
        cols = df.columns

        # Each item --> { 'timestamp: ..., 'ax': ..., 'ay': ..., 'az':... }
        return [{
            col: item[col] for col in cols
        } for i, item in df.iterrows()]

    def _convert_smartwatch_data_to_csv_format(self, json_data):
        accelerometer_data = json_data['sw_accelerometer']
        gyroscope_data = json_data['sw_gyroscope']
        barometer_data = json_data['sw_pressure']

        json_data['sw_accelerometer'] = smartwatch_data_converter.convert_smartwatch_accelerometer_data_to_csv(accelerometer_data)
        json_data['sw_gyroscope'] = smartwatch_data_converter.convert_smartwatch_gyroscope_data_to_csv(gyroscope_data)
        json_data['sw_barometer'] = smartwatch_data_converter.convert_smartwatch_pressure_data_to_csv(barometer_data)

        return json_data