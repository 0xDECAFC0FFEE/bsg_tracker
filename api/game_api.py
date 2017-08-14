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
import json
from common.endpoint_input import pop_str_arg, pop_str_args, pop_int_arg, pop_int_args, pop_rest_args, log
from common import game_rules

def games_to_json(session, games):

    output = []
    cylons = session.query(Player.game_id, User.name, Player.character, Player.phase).join(Cylon, Cylon.player_id==Player.player_id)\
    .filter(Player.game_id.in_([game.game_id for game in games])).join(User, User.user_id == Player.user_id).all()

    humans = session.query(Player.game_id, User.name, Player.character, Player.phase).join(Human, Human.player_id==Player.player_id)\
    .filter(Player.game_id.in_([game.game_id for game in games])).join(User, User.user_id == Player.user_id).all()

    cylon_leaders = session.query(Player.game_id, User.name, Player.character, Player.phase).join(CylonLeader, CylonLeader.player_id==Player.player_id)\
    .filter(Player.game_id.in_([game.game_id for game in games])).join(User, User.user_id == Player.user_id).all()

    cylons_in_game = defaultdict(list)
    humans_in_game = defaultdict(list)
    cylon_leaders_in_game = defaultdict(list)
    for cylon in cylons:
        cylons_in_game[cylon[0]].append({"name": cylon[1], "character": cylon[2], "phase": cylon[3]})
    for human in humans:
        humans_in_game[human[0]].append({"name": human[1], "character": human[2], "phase": human[3]})
    for cylon_leader in cylon_leaders:
        cylon_leaders_in_game[cylon_leader[0]].append({"name": cylon_leader[1], "character": cylon_leader[2], "phase": cylon_leader[3]})

    for game in games:
        details = {
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
        """
        inputs:
            joshua_horowitz: [{"loyalty": "human", "character": "helo"}, {"loyalty": "cylon", "character": "helo"}]
            andy_tong: [{"loyalty": "human", "character": "starbuck"}, {"loyalty": "human", "character": "roslin"}]
            lucas_tong: [{"loyalty": "human", "character": "s tigh"}] 
                # if only one phase is logged, it's automatically copied to the second phase
            anthony_ebbs: [{"loyalty": "cylon_leader", "character": "six"}]
            ...
            loss_condition: won 
                # can be one of: ["won", "galactica", "fuel", "food", "morale", "population", "heavy_raider"]. see LOSS CONDITION in bsg_info_orm
            fuel_left: 4
            food_left: 3
            morale_left: 4
            population_left: 5
            distance_left: 0
            used_pegasus: True
            used_exodus: True
            used_daybreak: True
            notes: asdfasdfasdf
        """

        loss_condition = pop_str_arg(self, "loss_condition", default=None)
        fuel_left = pop_str_arg(self, "fuel_left", default=None)
        food_left = pop_str_arg(self, "food_left", default=None)
        morale_left = pop_str_arg(self, "morale_left", default=None)
        population_left = pop_str_arg(self, "population_left", default=None)
        distance_left = pop_str_arg(self, "distance_left", default=None)

        used_pegasus = pop_str_arg(self, "used_pegasus", default=None)
        used_exodus = pop_str_arg(self, "used_exodus", default=None)
        used_daybreak = pop_str_arg(self, "used_daybreak", default=None)

        notes = pop_str_arg(self, "notes", default=None)

        rest_args = pop_rest_args(self)
        players = []
        for user, character in rest_args.items():
            characters_info = json.loads(character[0])
            players.append(game_rules.Player(user, characters_info))

        with sql.db_write_session() as session:
            new_game = Game(
                loss_condition=loss_condition,
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

            for player in players:
                user = session.query(User).filter(User.name == player.name).one()
                for char in player.characters:
                    new_player = Player(game_id=new_game.game_id, user_id=user.user_id, character=char.character, phase=char.phase)
                    session.add(new_player)
                    session.flush()

                    if char.loyalty == "human":
                        new_player = Human(player_id = new_player.player_id)
                    elif char.loyalty == "cylon":
                        new_player = Cylon(player_id = new_player.player_id)
                    elif char.loyalty == "cylon_leader":
                        new_player = CylonLeader(player_id = new_player.player_id)
                    session.add(new_player)
        self.write({"success": True})


class GetAllHandler(tornado.web.RequestHandler):
    def post(self):
        with sql.db_write_session() as session:
            games = session.query(Game).all()
            games = games_to_json(session, games)
        self.write({"success": True, "games": games})


class DeleteGameHandler(tornado.web.RequestHandler):
    def post(self):
        game_ids = pop_int_args(self, "game_id")

        with sql.db_write_session() as session:
            if game_ids == [u"*"]:
                session.query(Game).delete()
            else:
                for game_id in game_ids:
                    session.query(Game).filter(Game.game_id == game_id).delete()
        self.write({"success": True})
