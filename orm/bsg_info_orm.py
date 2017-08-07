import datetime
import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, MetaData, PrimaryKeyConstraint, ForeignKeyConstraint, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import BIGINT, BLOB, BOOLEAN, CHAR, DATETIME, FLOAT, INT, SMALLINT, SMALLINT, TEXT, TIMESTAMP, VARCHAR, Enum
from common import game_rules

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

CHARACTERS = Enum(*(
    list(game_rules.CYLON_LEADER_CHARACTERS)+
    list(game_rules.NON_CYLON_LEADER_CHARACTERS)), name="characters")

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
    player_id = Column(INT, primary_key=True, autoincrement=True)
    game_id = Column(INT, ForeignKey('game.game_id', ondelete='CASCADE', onupdate='CASCADE', name='player.game_id game.game_id fk'))
    user_id = Column(INT, ForeignKey('user.user_id', name='player.user_id user.user_id fk', onupdate='CASCADE'))
    phase = Column(INT)
    character = Column(CHARACTERS)
    __tablename__ = "player"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
        UniqueConstraint('game_id', 'user_id', 'phase', name='unique id constraint player')
    )
    user = relationship("User")
    game = relationship("Game")


class Cylon(Base):
    player_id = Column(INT, ForeignKey('player.player_id', ondelete='CASCADE', onupdate='CASCADE', name='cylon player fk'), primary_key=True)
    __tablename__ = "cylon"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    player = relationship("Player")


class Human(Base):
    player_id = Column(INT, ForeignKey('player.player_id', ondelete='CASCADE', onupdate='CASCADE', name='human player fk'), primary_key=True)
    __tablename__ = "human"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    player = relationship("Player")


class CylonLeader(Base):
    player_id = Column(INT, ForeignKey('player.player_id', ondelete='CASCADE', onupdate='CASCADE', name='cylon_leader player fk'), primary_key=True)
    __tablename__ = "cylon_leader"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    player = relationship("Player")
