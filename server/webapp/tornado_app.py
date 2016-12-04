import tornado.ioloop as ioloop
import tornado.web as web
from webapp.handler.smartphone_recorder_handler import SmartphoneRecorderHandler
from webapp.handler.smartwatch_notifier_handler import SmartwatchNotifierHandler
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler
from webapp.handler.smartwatch_recorder_handler import SmartwatchRecorderHandler
from webapp.handler.client_raw_data_handler import ClientRawDataHandler
from webapp.util.logger import web_logger as LOGGER
from webapp.service.raw_data_service import RawDataService
from webapp.service.sensory_data_service import SensoryDataService
import webapp.web_config as CONFIG


if __name__ == '__main__':
    services = {
        'raw_data_service': RawDataService(),
        'sensory_data_service': SensoryDataService()
    }

    app = web.Application([
        (r"/", SmartphoneRecorderHandler),
        (r"/smartwatch/notify", SmartwatchNotifierHandler),
        (r"/smartwatch/ws", SmartwatchWebsocketHandler),
        (r"/smartwatch/upload", SmartwatchRecorderHandler),
        (r"/client/raw", ClientRawDataHandler)
    ], debug=True, **services)

    LOGGER.info("Starting server at port {}...".format(CONFIG.SERVER_PORT_NUMBER))
    app.listen(CONFIG.SERVER_PORT_NUMBER)
    ioloop.IOLoop.current().start()