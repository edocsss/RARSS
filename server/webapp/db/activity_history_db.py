from webapp.db.base_db import BaseDb
import webapp.web_config as CONFIG


"""
Handles DB actions related to the Activity History collections.
"""


class ActivityHistoryDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self)

    def insert_activity_history(self, activity_history):
        self._db[CONFIG.ACTIVITY_HISTORY_COLLECTION].insert_one(activity_history)

    def get_activity_history_by_time(self, start_time):
        pass