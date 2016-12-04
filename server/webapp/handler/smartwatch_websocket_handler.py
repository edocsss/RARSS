from tornado.websocket import WebSocketHandler
from webapp.util.logger import web_logger as LOGGER


class SmartwatchWebsocketHandler(WebSocketHandler):
    clients = []

    def open(self):
        LOGGER.info("WebSocket opened!")
        SmartwatchWebsocketHandler.clients.append(self)

    def on_message(self, message):
        LOGGER.info(message)

    def on_close(self):
        LOGGER.info("WebSocket closed!")
        SmartwatchWebsocketHandler.clients.remove(self)

    def check_origin(self, origin):
        return True

    @classmethod
    def broadcast(cls, message):
        LOGGER.info("Writing message: {}".format(message))
        for c in cls.clients:
            c.write_message(message)