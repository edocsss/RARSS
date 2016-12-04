from webapp.db.base_db import BaseDb
import webapp.web_config as CONFIG


class ActivityRecognitionQueueDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self, CONFIG.ACTIVITY_RECOGNITION_QUEUE_COLLECTION)

