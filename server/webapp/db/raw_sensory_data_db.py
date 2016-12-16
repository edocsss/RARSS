from webapp.db.base_db import BaseDb
import webapp.web_config as CONFIG


"""
Handles DB actions related to the Raw Sensory Data collections (both Smartphone and Smartwatch).
"""


class RawSensoryDataDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self)

    def _insert_raw_data(self, collection_name, uuid, raw_data_list):
        for item in raw_data_list:
            item['uuid'] = uuid

        self._db[collection_name].insert_many(raw_data_list)

    def _get_raw_data_by_uuid(self, collection_name, uuid):
        return self._db[collection_name].find({ 'uuid': uuid })

    def insert_sp_raw_accelerometer_data(self, uuid, sp_accelerometer_data_list):
        self._insert_raw_data(CONFIG.SP_RAW_ACCELEROMETER_DATA_COLLECTION, uuid, sp_accelerometer_data_list)

    def insert_sw_raw_accelerometer_data(self, uuid, sw_accelerometer_data_list):
        self._insert_raw_data(CONFIG.SW_RAW_ACCELEROMETER_DATA_COLLECTION, uuid, sw_accelerometer_data_list)

    def get_sp_raw_accelerometer_data_by_uuid(self, uuid):
        return list(self._get_raw_data_by_uuid(CONFIG.SP_RAW_ACCELEROMETER_DATA_COLLECTION, uuid))

    def get_sw_raw_accelerometer_data_by_uuid(self, uuid):
        return list(self._get_raw_data_by_uuid(CONFIG.SW_RAW_ACCELEROMETER_DATA_COLLECTION, uuid))