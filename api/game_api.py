import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import enable_pretty_logging

from orm.bsg_info_orm import User, Game, Cylon, Human, CylonLeader
from common import sql

loss_condition_map = {
    "galactica": 1,
    "fuel": 2,
    "food": 3,
    "morale": 4,
    "population": 5,
    "heavy_raider": 6,
    None: None
}
loss_condition_map.update({v:k for k, v in loss_condition_map.iteritems()})


def games_to_json(games):
    output = []
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
        
        cylons = [cylon.user.name for cylon in game.cylons]
        humans = [human.user.name for human in game.humans]
        cylon_leaders = [cylon_leader.user.name for cylon_leader in game.cylon_leaders]

        output.append({
            "date": str(game.date),
            "game_id": game.game_id,
            "loss_condition": loss_condition_map[game.loss_condition],
            "details": details,
            "cylons": cylons,
            "humans": humans,
            "cylon_leaders": cylon_leaders,
        })
    return output


class AddGameHandler(tornado.web.RequestHandler):
    def post(self):
        cylon_user_names = self.get_arguments(name="cylons", strip=True)
        human_user_names = self.get_arguments(name="humans", strip=True)
        cylon_leader_user_names = self.get_arguments(name="cylon_leaders", strip=True)

        for cylon_user_name in cylon_user_names:
            assert cylon_user_name not in human_user_names
            assert cylon_user_name not in cylon_leader_user_names
        
        for human_user_name in human_user_names:
            assert human_user_name not in cylon_leader_user_names

        [loss_condition] = self.get_arguments(name="loss_condition", strip=True) or [None]
        loss_condition = loss_condition_map[loss_condition]
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
            session.commit()
            session.flush()

            for cylon_user_name in cylon_user_names:
                user = session.query(User).filter(User.name == cylon_user_name).one()
                new_cylon = Cylon(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_cylon)
            for human_user_name in human_user_names:
                user = session.query(User).filter(User.name == human_user_name).one()
                new_human = Human(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_human)
            for cylon_leader_user_name in cylon_leader_user_names:
                user = session.query(User).filter(User.name == cylon_leader_user_name).one()
                new_cylon_leader = CylonLeader(game_id=new_game.game_id, user_id=user.user_id)
                session.add(new_cylon_leader)
        self.write({"success": True})


class GetAllHandler(tornado.web.RequestHandler):
    def post(self):
        with sql.db_write_session() as session:
            games_raw = session.query(Game).all()
            games = games_to_json(games_raw)
        self.write({"success": True, "games": games})


class DeleteGameHandler(tornado.web.RequestHandler):
    def post(self):
        game_id = self.get_argument(name="game_id", strip=True)
        
        with sql.db_write_session() as session:
            session.query(Game).filter(Game.game_id == game_id).delete()
        self.write({"success": True})
