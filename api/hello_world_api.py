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
        self.render("../templates/newgame_template.html", title="New Game")
    def post(self):
        print("player name: " + str(self.get_body_argument("playerName")))
        print("character name: " + str(self.get_body_argument("characterName")))

