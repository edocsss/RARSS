import tornado.ioloop as ioloop
import tornado.web as web
from webapp.handler.smartphone_handler import SmartphoneHandler
from webapp.handler.smartwatch_notifier_handler import SmartwatchNotifierHandler
from webapp.handler.smartwatch_websocket_handler import SmartwatchWebsocketHandler
from webapp.handler.smartwatch_handler import SmartwatchHandler
from webapp.handler.client_raw_data_handler import ClientRawDataHandler

PORT_NUMBER = 5000

if __name__ == '__main__':
    app = web.Application([
        (r"/", SmartphoneHandler),
        (r"/smartwatch/notify", SmartwatchNotifierHandler),
        (r"/smartwatch/ws", SmartwatchWebsocketHandler),
        (r"/smartwatch/upload", SmartwatchHandler),
        (r"/client/raw", ClientRawDataHandler)
    ], debug=True)

    print("Starting server at port {}...".format(PORT_NUMBER))
    app.listen(PORT_NUMBER)
    ioloop.IOLoop.current().start()