import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import enable_pretty_logging
from api.hello_world_api import HelloWorldHandler
from api.echo_api import EchoHandler
from api.user_api import AddUserHandler
from api.user_api import UpdateUserHandler
from api.user_api import GetUsersHandler
from api.user_api import GetHumanGamesHandler
from api.user_api import GetCylonGamesHandler
from api.user_api import GetNameHandler
from api.user_api import GetIdHandler
from api.game_api import AddGameHandler
from api.game_api import GetAllHandler
from api.game_api import DeleteGameHandler
from orm import bsg_info_orm

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
enable_pretty_logging()

def make_app():
    return tornado.web.Application([
        (r"/api/helloWorld", HelloWorldHandler),
        (r"/api/echo", EchoHandler),
        (r"/api/user/add", AddUserHandler),
        (r"/api/user/update", UpdateUserHandler),
        (r"/api/user/humanGames", GetHumanGamesHandler),
        (r"/api/user/cylonGames", GetCylonGamesHandler),
        (r"/api/user/all", GetUsersHandler),
        (r"/api/user/getName", GetNameHandler),
        (r"/api/user/getId", GetIdHandler),
        (r"/api/game/add", AddGameHandler),
        (r"/api/game/all", GetAllHandler),
        (r"/api/game/delete", DeleteGameHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
