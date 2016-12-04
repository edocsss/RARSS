from pymongo import *
from webapp import web_config as CONFIG
from webapp.util.logger import web_logger as LOGGER


class BaseDb():
    def __init__(self, db_name):
        LOGGER.info('Connecting to MongoDB...')
        try:
            self._client = MongoClient(CONFIG.MONGODB_URI)
            self._db = self._client[CONFIG.DB_NAME]
            self._collection = self._db[db_name]
            LOGGER.info('Connected to MongoDB!')

        except Exception as e:
            LOGGER.error('Connection to MongoDB failed!')
            LOGGER.error(e)