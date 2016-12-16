from tornado.websocket import WebSocketHandler

from util.logger import web_logger as LOGGER


"""
Handles WebSocket connection and communication with the Smartwatch application.
"""


class SmartwatchWebsocketHandler(WebSocketHandler):
    clients = []

    def open(self):
        LOGGER.info("WebSocket for Smartwatch opened!")
        SmartwatchWebsocketHandler.clients.append(self)

    def on_message(self, message):
        LOGGER.info(message)

    def on_close(self):
        LOGGER.info("WebSocket for Smartwatch closed!")
        SmartwatchWebsocketHandler.clients.remove(self)

    def check_origin(self, origin):
        return True

    @classmethod
    def broadcast(cls, message):
        LOGGER.info("Writing message to Smartwatch: {}".format(message))
        for c in cls.clients:
            c.write_message(message)