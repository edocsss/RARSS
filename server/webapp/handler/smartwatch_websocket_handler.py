from tornado.websocket import WebSocketHandler

class SmartwatchWebsocketHandler(WebSocketHandler):
    clients = []

    def open(self):
        print("WebSocket opened!")
        SmartwatchWebsocketHandler.clients.append(self)

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("WebSocket closed!")
        SmartwatchWebsocketHandler.clients.remove(self)

    def check_origin(self, origin):
        return True

    @classmethod
    def broadcast(cls, message):
        print("Writing message: {}".format(message))
        for c in cls.clients:
            c.write_message(message)