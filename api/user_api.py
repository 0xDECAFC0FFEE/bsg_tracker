import tornado.ioloop
import tornado.web
import sys
import os
from sqlalchemy import join
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tornado.log import enable_pretty_logging
from orm.bsg_info_orm import User, Human, Cylon, Game, CylonLeader, Player
from api.game_api import games_to_json
from common import sql
import logging
from common.endpoint_input import pop_str_arg, pop_str_args, pop_int_arg, pop_int_args

def get_user(session, user_name):
    return session.query(User).filter(User.name == user_name)

class UpdateUserHandler(tornado.web.RequestHandler):
    def post(self):
        old_user_name = pop_str_arg(self, "user_name", "^\w+$")
        new_user_name = pop_str_arg(self, "new_user_name", "^\w+$")

        try:
            with sql.db_write_session() as session:
                user = get_user(session, old_user_name).one()
                user.name = new_user_name
        except IntegrityError as e:
            raise Exception("user \"%s\" already exists" % new_user_name)
        except NoResultFound as e:
            raise Exception("user \"%s\" not found" % old_user_name)
        self.write({"success": True})


class AddUserHandler(tornado.web.RequestHandler):
    def post(self):
        user_names = pop_str_args(self, "user_name", "^\w+$")

        try:
            with sql.db_write_session() as session:
                for user_name in user_names:
                    new_user = User(name=user_name)
                    session.add(new_user)
        except IntegrityError as e:
            raise Exception("user \"%s\" already exists" % user_name)
        self.write({"success": True})


class GetUsersHandler(tornado.web.RequestHandler):
    def post(self):
        with sql.db_read_session() as session:
            users = session.query(User.name).all()
            users = [user for [user] in users]
        self.write({"success": True, "users":users})


class GetNameHandler(tornado.web.RequestHandler):
    def post(self):
        user_id = pop_int_arg(self, "user_id")
        try:
            with sql.db_read_session() as session:
                [user] = session.query(User.name).filter(User.user_id==user_id).one()
            self.write({"success": True, "user":user})
        except NoResultFound as a:
            raise Exception("user with id %s not found" % user_id[0])

class GetIdHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = pop_str_arg(self, "user_name", "^\w+$")
        
        with sql.db_read_session() as session:
            user = get_user(session, user_name).one()
            user_id = user.user_id
        self.write({"success": True, "user":user_id})


class GetHumanGamesHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = pop_str_arg(self, "user_name", "^\w+$")

        with sql.db_read_session() as session:
            games = session.query(Game).join(Player, Player.game_id==Game.game_id).join(Human, Human.player_id == Player.player_id).join(User, Player.user_id==User.user_id).filter(User.name==user_name).all()
            games = games_to_json(session, games)
        self.write({"success": True, "games":games})


class GetCylonGamesHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = pop_str_arg(self, "user_name", "^\w+$")

        with sql.db_read_session() as session:
            games = session.query(Game).join(Player, Player.game_id==Game.game_id).join(Cylon, Cylon.player_id == Player.player_id).join(User, Player.user_id==User.user_id).filter(User.name==user_name).all()
            games = games_to_json(session, games)
        self.write({"success": True, "games":games})


class GetCylonLeaderGamesHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = pop_str_arg(self, "user_name", "^\w+$")

        with sql.db_read_session() as session:
            games = session.query(Game).join(Player, Player.game_id==Game.game_id).join(CylonLeader, CylonLeader.player_id == Player.player_id).join(User, Player.user_id==User.user_id).filter(User.name==user_name).all()
            games = games_to_json(session, games)
        self.write({"success": True, "games":games})

class GetAllGamesHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = pop_str_arg(self, "user_name", "^\w+$")

        with sql.db_read_session() as session:
            games = session.query(Game).join(Player, Player.game_id==Game.game_id).join(User, Player.user_id==User.user_id).filter(User.name==user_name).all()
            games = games_to_json(session, games)
        self.write({"success": True, "games":games})