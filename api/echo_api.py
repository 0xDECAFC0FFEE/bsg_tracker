import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import enable_pretty_logging

# sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
# from orm import BsgInfoOrm


class EchoHandler(tornado.web.RequestHandler):
    def post(self):
        echo = "echo"
        echo = self.get_argument(name=echo, strip=True)
        self.write(echo)