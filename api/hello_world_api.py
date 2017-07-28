import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import enable_pretty_logging

# sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
# from orm import BsgInfoOrm


class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self): 
        self.write("Helo, world")