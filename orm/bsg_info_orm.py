import datetime
import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, MetaData, PrimaryKeyConstraint, ForeignKeyConstraint, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import BIGINT, BLOB, BOOLEAN, CHAR, DATETIME, FLOAT, INT, SMALLINT, SMALLINT, TEXT, TIMESTAMP, VARCHAR, Enum
# Base.metadata.reflect(some_engine)

DATABASE_NAME = "bsg_info"

my_metadata = MetaData(schema=DATABASE_NAME)
Base = declarative_base(metadata=my_metadata)

LOSS_CONDITIONS = Enum(*["won", "galactica", "fuel", "food", "morale", "population", "heavy_raider"], name="loss_conditions")

""" 
character name creation rules:
    1. use nickname if possible, else use last name (eg Lee "Apollo" Adama vs William Adama)
    2. if name conflict, prepend first letter of first name
    3. if alternate version (included in daybreak expansion), append "A"
"""

CHARACTERS = Enum(*[
    "ADAMA", "S TIGH", "BOOMER", "APOLLO", "STARBUCK", "VALERII", "CHIEF", "ZAREK", "BALTAR", "ROSLIN",     # original
    "CAIN", "HELO", "DEE", "KAT", "E TIGH", # pegasus
    "GAETA", "ANDERS", "CALLY", "FOSTER",   # exodus
    "HOSHI", "HOT DOG", "DOC", "APPOLO A", "ZAREK A", "BALTAR A", "LAMPKIN",   # daybreak
    ], name="characters")

class User(Base):
    __tablename__ = "user"
    __table_args__=(
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        }
    )
    user_id = Column(INT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(30), nullable=False, unique=True)


class Game(Base):
    __tablename__ = "game"
    __table_args__ = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        }
    )
    game_id = Column(INT, primary_key=True, autoincrement=True)
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)
    loss_condition = Column(LOSS_CONDITIONS, nullable=False)
    raptors_left = Column(SMALLINT, nullable=True)
    vipers_left = Column(SMALLINT, nullable=True)
    
    fuel_left = Column(SMALLINT, nullable=True)
    food_left = Column(SMALLINT, nullable=True)
    morale_left = Column(SMALLINT, nullable=True)
    population_left = Column(SMALLINT, nullable=True)
    distance_left = Column(SMALLINT, nullable=True)

    used_pegasus = Column(BOOLEAN, nullable=True)
    used_daybreak = Column(BOOLEAN, nullable=True)
    used_exodus = Column(BOOLEAN, nullable=True)

    notes = Column(VARCHAR(60), nullable=True)

    players = relationship("Player")


class Player(Base):
    game_id = Column(INT, ForeignKey('game.game_id', ondelete='CASCADE', name='player.game_id game.game_id fk'), primary_key=True)
    user_id = Column(INT, ForeignKey('user.user_id', name='player.user_id user.user_id fk'), primary_key=True)
    character = Column(CHARACTERS, nullable=True)
    __tablename__ = "player"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    user = relationship("User")
    game = relationship("Game")


class Cylon(Base):
    game_id = Column(INT, ForeignKey('player.game_id', ondelete='CASCADE', name='cylon.game_id player.game_id fk'), primary_key=True)
    user_id = Column(INT, ForeignKey('player.user_id', ondelete='CASCADE', name='cylon.user_id player.user_id fk'), primary_key=True)
    __tablename__ = "cylon"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    player = relationship("Player", foreign_keys=[user_id], primaryjoin="and_(Cylon.game_id == Player.game_id, Cylon.user_id == Player.user_id)")


class Human(Base):
    game_id = Column(INT, ForeignKey('player.game_id', ondelete='CASCADE', name='human.game_id player.game_id fk'), primary_key=True)
    user_id = Column(INT, ForeignKey('player.user_id', ondelete='CASCADE', name='human.user_id player.user_id fk'), primary_key=True)
    __tablename__ = "human"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    player = relationship("Player", primaryjoin="and_(Human.game_id == Player.game_id, Human.user_id == Player.user_id)")


class CylonLeader(Base):
    game_id = Column(INT, ForeignKey('player.game_id', ondelete='CASCADE', name='cylon_leader.game_id player.game_id fk'), primary_key=True)
    user_id = Column(INT, ForeignKey('player.user_id', ondelete='CASCADE', name='cylon_leader.user_id player.user_id fk'), primary_key=True)
    __tablename__ = "cylon_leader"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    player = relationship("Player", primaryjoin="and_(CylonLeader.game_id == Player.game_id, CylonLeader.user_id == Player.user_id)")
