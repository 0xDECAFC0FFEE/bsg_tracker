import tornado.ioloop
import tornado.web
import sys
import os
import re
from sqlalchemy import join
from tornado.log import enable_pretty_logging

from orm.bsg_info_orm import User, Human, Cylon, Game
from api.game_api import games_to_json
from common import sql


def get_names(request_handler, argument_name="user_name"):
    user_names = request_handler.get_arguments(name=argument_name, strip=True)
    for user_name in user_names:
        assert re.match("^\w+$", user_name), user_name
    return user_names


def get_name(request_handler, argument_name="user_name"):
    user_names = get_names(request_handler, argument_name)
    assert len(user_names) == 1, user_names
    return user_names[0]


def get_user(session, user_name):
    return session.query(User).filter(User.name == user_name)


class UpdateUserHandler(tornado.web.RequestHandler):
    def post(self):
        old_user_name = get_name(self, argument_name="user_name")
        new_user_name = get_name(self, argument_name="new_user_name")
        
        with sql.db_write_session() as session:
            user = get_user(session, old_user_name).one()
            user.name = new_user_name
        self.write({"success": True})


class AddUserHandler(tornado.web.RequestHandler):
    def post(self):
        user_names = get_names(self)
        
        with sql.db_write_session() as session:
            for user_name in user_names:
                users = session.query(User).filter(User.name == user_name).all()
                assert not users
                new_user = User(name=user_name)
                session.add(new_user)
        self.write({"success": True})


class GetUsersHandler(tornado.web.RequestHandler):
    def post(self):
        with sql.db_write_session() as session:
            users = session.query(User.name).all()
            users = [user for [user] in users]
        self.write({"success": True, "users":users})


class GetNameHandler(tornado.web.RequestHandler):
    def post(self):
        user_id = self.get_arguments(name="user_id", strip=True)
        
        with sql.db_write_session() as session:
            [user] = session.query(User.name).filter(User.user_id==user_id).one()
        self.write({"success": True, "user":user})


class GetIdHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = get_name(self)
        
        with sql.db_write_session() as session:
            user = get_user(session, user_name).one()
            user_id = user.user_id
        self.write({"success": True, "user":user_id})


class GetHumanGamesHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = get_name(self)

        with sql.db_write_session() as session:
            games = session.query(Game).join(Human, Human.game_id==Game.game_id).join(User, Human.user_id==User.user_id).filter(User.name==user_name).all()
            games = games_to_json(games)
        self.write({"success": True, "games":games})


class GetCylonGamesHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = get_name(self)

        with sql.db_write_session() as session:
            games = session.query(Game).join(Cylon, Cylon.game_id==Game.game_id).join(User, Cylon.user_id==User.user_id).filter(User.name==user_name).all()
            games = games_to_json(games)
        self.write({"success": True, "games":games})

