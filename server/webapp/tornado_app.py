import signal
import threading

import tornado.ioloop as ioloop
import tornado.web as web

import webapp.web_config as CONFIG
from util.logger import web_logger as LOGGER
from webapp.handler.client_raw_data_handler import ClientRawDataHandler
from webapp.handler.client_websocket_handler import ClientWebsocketHandler
from webapp.handler.smartphone_monitoring_handler import SmartphoneMonitoringHandler
from webapp.handler.smartphone_recording_handler import SmartphoneRecordingHandler
from webapp.handler.smartwatch_monitoring_handler import SmartwatchMonitoringHandler
from webapp.handler.smartwatch_monitoring_notifier_handler import SmartwatchMonitoringNotifierHandler
from webapp.handler.smartwatch_recording_handler import SmartwatchRecordingHandler
from webapp.handler.smartwatch_recording_notifier_handler import SmartwatchRecordingNotifierHandler
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler
from webapp.service.raw_data_service import RawDataService
from webapp.service.real_time_monitoring_service import RealTimeMonitoringService
from webapp.service.sensory_data_service import SensoryDataService
from webapp.worker.activity_recognizer_worker import ActivityRecognizerWorker


if __name__ == '__main__':
    services = {
        'raw_data_service': RawDataService(),
        'sensory_data_service': SensoryDataService(),
        'real_time_monitoring_service': RealTimeMonitoringService()
    }

    app = web.Application([
        (r"/smartphone/recording", SmartphoneRecordingHandler),
        (r"/smartphone/monitoring", SmartphoneMonitoringHandler),
        (r"/smartwatch/recording/notify", SmartwatchRecordingNotifierHandler),
        (r"/smartwatch/monitoring/notify", SmartwatchMonitoringNotifierHandler),
        (r"/smartwatch/ws", SmartwatchWebsocketHandler),
        (r"/smartwatch/recording", SmartwatchRecordingHandler),
        (r"/smartwatch/monitoring", SmartwatchMonitoringHandler),
        (r"/client/raw", ClientRawDataHandler),
        (r"/client/ws", ClientWebsocketHandler)
    ], debug=True, **services)

    activity_recognizer_worker = ActivityRecognizerWorker()
    worker_thread = threading.Thread(target=activity_recognizer_worker.start)
    worker_thread.start()

    def kill_activity_recognizer_worker(signum, handler):
        activity_recognizer_worker.stop()
        worker_thread.join()

        io_loop = ioloop.IOLoop.instance()
        io_loop.stop()
        LOGGER.info('Shutting down server!')

    signal.signal(signal.SIGQUIT, kill_activity_recognizer_worker)
    signal.signal(signal.SIGTERM, kill_activity_recognizer_worker)
    signal.signal(signal.SIGINT, kill_activity_recognizer_worker)

    LOGGER.info("Starting server at port {}...".format(CONFIG.SERVER_PORT_NUMBER))
    app.listen(CONFIG.SERVER_PORT_NUMBER)
    ioloop.IOLoop.current().start()