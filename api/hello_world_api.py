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
            "teams__starting",
            "teams__sleeper",
            "game__expansions",
            "game__winner",
            "results__resources--fuel",
            "results__resources--food",
            "results__resources--morale",
            "results__resources--population",
            "results__stats--raptors",
            "results__stats--vipers",
            "results__stats--distance",
        ]

        form_map = {}

        post_str = "{"
        for key in keys:
            try:
                arg = str(self.get_body_arguments(key))
                print(" >>> " + key + "  " + str(arg))
                form_map[key] = arg
            except (tornado.web.MissingArgumentError):
                print(" >>> problem with " + key)

        print(form_map)
        self.write(form_map)





