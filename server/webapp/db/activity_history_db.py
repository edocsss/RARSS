from webapp.db.base_db import BaseDb
import webapp.web_config as CONFIG


class ActivityHistoryDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self, CONFIG.ACTIVITY_HISTORY_COLLECTION)


    def insert_activity_history(self, activity_history):
        pass


    def get_activity_history_by_time(self, start_time):
        pass