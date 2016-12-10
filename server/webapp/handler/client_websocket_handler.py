from tornado.websocket import WebSocketHandler

from util.logger import web_logger as LOGGER


class ClientWebsocketHandler(WebSocketHandler):
    clients = []

    def open(self):
        LOGGER.info("WebSocket for Clients opened!")
        ClientWebsocketHandler.clients.append(self)

    def on_message(self, message):
        LOGGER.info(message)

    def on_close(self):
        LOGGER.info("WebSocket for Clients closed!")
        ClientWebsocketHandler.clients.remove(self)

    def check_origin(self, origin):
        return True

    @classmethod
    def broadcast(cls, message):
        LOGGER.info("Writing message to clients: {}".format(message))
        for c in cls.clients:
            c.write_message(message)