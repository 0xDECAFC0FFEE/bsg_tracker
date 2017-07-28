import datetime
import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, MetaData, PrimaryKeyConstraint, ForeignKeyConstraint, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import BIGINT, BLOB, BOOLEAN, CHAR, DATETIME, FLOAT, INT, SMALLINT, SMALLINT, TEXT, TIMESTAMP, VARCHAR
# Base.metadata.reflect(some_engine)

DATABASE_NAME = "bsg_info"

my_metadata = MetaData(schema=DATABASE_NAME)
Base = declarative_base(metadata=my_metadata)


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
    loss_condition = Column(SMALLINT, nullable=True)
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

    cylons = relationship("Cylon")
    humans = relationship("Human")


class Cylon(Base):
    game_id = Column(INT, ForeignKey('game.game_id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(INT, ForeignKey('user.user_id'), primary_key=True)
    __tablename__ = "cylon"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    user = relationship("User")


class Human(Base):
    game_id = Column(INT, ForeignKey('game.game_id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(INT, ForeignKey('user.user_id'), primary_key=True)
    __tablename__ = "human"
    __table_args = (
        {
            "schema": DATABASE_NAME,
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8",
        },
    )
    user = relationship("User")