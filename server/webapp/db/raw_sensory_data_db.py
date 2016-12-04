from webapp.db.base_db import BaseDb
import webapp.web_config as CONFIG


class RawSensoryDataDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self, CONFIG.RAW_SENSORY_DATA_COLLECTION)


    def insert_raw_data(self, raw_data_list):
        pass


    def get_raw_data_by_time(self, start_time, end_time):
        pass


    def delete_raw_data_by_time(self, start_time, end_time):
        pass