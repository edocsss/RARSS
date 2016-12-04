from pymongo import *
from webapp import web_config as CONFIG
from webapp.util.logger import web_logger as LOGGER


class BaseDb():
    _client = None

    def init(self):
        print('Connecting to MongoDB...')
        try:
            self._client = MongoClient(CONFIG.MONGODB_URI)
            LOGGER.info('Connected to MongoDB!')

        except Exception as e:
            LOGGER.error('Connection to MongoDB failed!')
            LOGGER.error(e)