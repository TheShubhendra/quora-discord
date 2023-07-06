from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Guild(Base):
    __tablename__ = "guilds"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    update_channel = Column(BigInteger)
    watchers = relationship("Watcher", backref="guild")


class Watcher(Base):
    __tablename__ = "watchers"
    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guilds.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    language = Column(String(10))
    user_id = Column(Integer, ForeignKey("users.id"))
    answer_count = Column(Integer, default=0)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger)
    discord_username = Column(String(100))
    quora_username = Column(String(100))
    follower_count = Column(Integer, default=0)
    access = Column(String(10), default="public")
    watchers = relationship("Watcher", backref="user")
    profiles = relationship("Profile", backref="user")


__all__ = [
    Base,
    Profile,
    Guild,
    User,
    Watcher,
]