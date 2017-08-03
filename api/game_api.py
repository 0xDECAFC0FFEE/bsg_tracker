import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import enable_pretty_logging
from collections import defaultdict


import logging
from sqlalchemy.sql import select
from sqlalchemy import and_, or_, desc
from orm.bsg_info_orm import User, Game, Cylon, Human, CylonLeader, Player
from common import sql


def games_to_json(session, games):

    output = []
    cylons = session.query(Cylon.game_id, User.name).filter(Cylon.game_id.in_([game.game_id for game in games])).join(User, User.user_id == Cylon.user_id).all()
    humans = session.query(Human.game_id, User.name).filter(Human.game_id.in_([game.game_id for game in games])).join(User, User.user_id == Human.user_id).all()
    cylon_leaders = session.query(CylonLeader.game_id, User.name).filter(CylonLeader.game_id.in_([game.game_id for game in games])).join(User, User.user_id == CylonLeader.user_id).all()

    cylons_in_game = defaultdict(list)
    humans_in_game = defaultdict(list)
    cylon_leaders_in_game = defaultdict(list)
    for cylon in cylons:
        cylons_in_game[cylon[0]].append(cylon[1])
    for human in humans:
        humans_in_game[human[0]].append(human[1])    
    for cylon_leader in cylon_leaders:
        cylon_leaders_in_game[cylon_leader[0]].append(cylon_leader[1])

    for game in games:
        details = {
            "raptors_left": game.raptors_left,
            "vipers_left": game.vipers_left,
            
            "fuel_left": game.fuel_left,
            "food_left": game.food_left,
            "morale_left": game.morale_left,
            "population_left": game.population_left,
            "distance_left": game.distance_left,

            "used_pegasus": game.used_pegasus,
            "used_daybreak": game.used_daybreak,
            "used_exodus": game.used_exodus,

            "notes": game.notes,
        }
        
        output.append({
            "date": str(game.date),
            "game_id": game.game_id,
            "loss_condition": game.loss_condition,
            "details": details,
            "cylons": cylons_in_game[game.game_id] if game.game_id in cylons_in_game else None,
            "humans": humans_in_game[game.game_id] if game.game_id in humans_in_game else None,
            "cylon_leaders": cylon_leaders_in_game[game.game_id] if game.game_id in cylon_leaders_in_game else None,
        })
    return output


class AddGameHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("add game")
        self.render("../templates/newgame_template.html", title="add game")

    def post(self):
        cylon_user_names = self.get_arguments(name="cylons", strip=True)
        human_user_names = self.get_arguments(name="humans", strip=True)
        cylon_leader_user_names = self.get_arguments(name="cylon_leaders", strip=True)

        [loss_condition] = self.get_arguments(name="loss_condition", strip=True) or [None]
        [raptors_left] = self.get_arguments(name="raptors_left", strip=True) or [None]
        [vipers_left] = self.get_arguments(name="vipers_left", strip=True) or [None]
        [fuel_left] = self.get_arguments(name="fuel_left", strip=True) or [None]
        [food_left] = self.get_arguments(name="food_left", strip=True) or [None]
        [morale_left] = self.get_arguments(name="morale_left", strip=True) or [None]
        [population_left] = self.get_arguments(name="population_left", strip=True) or [None]
        [distance_left] = self.get_arguments(name="distance_left", strip=True) or [None]

        [used_pegasus] = self.get_arguments(name="used_pegasus", strip=True) or [None]
        [used_exodus] = self.get_arguments(name="used_exodus", strip=True) or [None]
        [used_daybreak] = self.get_arguments(name="used_daybreak", strip=True) or [None]

        [notes] = self.get_arguments(name="notes", strip=True) or [None]
        
        with sql.db_write_session() as session:
            new_game = Game(
                loss_condition=loss_condition, 
                raptors_left = raptors_left, 
                vipers_left = vipers_left, 
                fuel_left = fuel_left, 
                food_left = food_left, 
                morale_left = morale_left, 
                population_left = population_left, 
                distance_left = distance_left,
                used_pegasus = used_pegasus != "False",
                used_exodus = used_exodus != "False",
                used_daybreak = used_daybreak != "False",
                notes = notes,
            )
            session.add(new_game)
            session.flush()

            for cylon_user_name in cylon_user_names:
                user = session.query(User).filter(User.name == cylon_user_name).one()
                new_player = Player(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_player)
                session.flush()
                new_cylon = Cylon(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_cylon)
            for human_user_name in human_user_names:
                user = session.query(User).filter(User.name == human_user_name).one()
                new_player = Player(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_player)
                session.flush()
                new_human = Human(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_human)
            for cylon_leader_user_name in cylon_leader_user_names:
                user = session.query(User).filter(User.name == cylon_leader_user_name).one()
                new_player = Player(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_player)
                session.flush()
                new_cylon_leader = CylonLeader(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_cylon_leader)
        self.write({"success": True})


class GetAllHandler(tornado.web.RequestHandler):
    def post(self):
        with sql.db_write_session() as session:
            games = session.query(Game).all()
            games = games_to_json(session, games)
        self.write({"success": True, "games": games})


class DeleteGameHandler(tornado.web.RequestHandler):
    def post(self):
        game_ids = self.get_arguments(name="game_id", strip=True)

        with sql.db_write_session() as session:
            if game_ids == [u"*"]:
                session.query(Game).delete()
            else:
                for game_id in game_ids:
                    session.query(Game).filter(Game.game_id == game_id).delete()
        self.write({"success": True})
