from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        self.set_header('Access-Control-Allow-Methods', '*')


    def options(self):
        # no body
        self.set_status(204)
        self.finish()