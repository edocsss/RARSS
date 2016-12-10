from webapp.db.base_db import BaseDb
import webapp.web_config as CONFIG
import pymongo


class WorkQueueDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self)

    def insert_uuid(self, uuid):
        self._db[CONFIG.WORK_QUEUE_COLLECTION].insert_one({
            'uuid': uuid
        })

    def remove_by_object_id(self, object_id):
        self._db[CONFIG.WORK_QUEUE_COLLECTION].remove({
            '_id': object_id
        })

    def get_next_uuid(self):
        next_uuid_doc = self._db[CONFIG.WORK_QUEUE_COLLECTION].find_one(sort=[('_id', pymongo.ASCENDING)])
        if next_uuid_doc is None:
            return

        self.remove_by_object_id(next_uuid_doc['_id'])
        return next_uuid_doc['uuid']


if __name__ == '__main__':
    db = WorkQueueDb()
    print(db.get_next_uuid())