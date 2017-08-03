import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import enable_pretty_logging

# sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
# from orm import BsgInfoOrm


class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self): 
        self.write("XD Helo, world")
        self.render("../templates/newgame_template.html", title="New Game")
    def post(self):

        keys = [
            "teams__player",
            "teams__character",
            "temp2"
        ]

        for key in keys:
            print(key + "  ")
            try:
                arg = str(self.get_body_argument(key))
            except (tornado.web.MissingArgumentError):
                arg = None
            print(key + "  " + str(arg))
            self.write(key + "  " + str(arg))


