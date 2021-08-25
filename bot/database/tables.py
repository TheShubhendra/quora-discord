from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Guild(Base):
    __tablename__ = "guild_data"
    guild_id = Column(String(50), primary_key=True)
    guild_name = Column(String(50))
    update_channel = Column(String(50))

    def __init__(
        self,
        guild_id,
        guild_name,
        update_channel,
    ):
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.update_channel = update_channel


class Watcher(Base):
    __tablename__ = "watcher_data"
    id = Column(Integer, primary_key=True)
    guild_id = Column(String(50))
    user_id = Column(Integer)

    def __init__(
        self,
        guild_id,
        user_id,
    ):
        self.guild_id = guild_id
        self.user_id = user_id


class Quoran(Base):
    __tablename__ = "quoran"
    user_id = Column(Integer, primary_key=True)
    discord_id = Column(String(50))
    discord_username = Column(String(100))
    quora_username = Column(String(50))
    follower_count = Column(Integer)
    answer_count = Column(Integer)
    access = Column(String(10))

    def __init__(
        self,
        discord_id,
        discord_username,
        quora_username,
        answer_count=0,
        follower_count=0,
        access="public",
    ):
        self.discord_id = discord_id
        self.discord_username = discord_username
        self.quora_username = quora_username
        self.follower_count = follower_count
        self.answer_count = answer_count
        self.access = access


__all__ = [
    Base,
    Guild,
    Watcher,
    Quoran,
]
