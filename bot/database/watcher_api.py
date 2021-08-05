from sqlalchemy import Column, String, Integer

from . import (
    BASE,
    ENGINE,
    SESSION,
)


class Watcher(BASE):
    __tablename__ = "watcher_data"
    guild_id = Column(String(50), primary_key=True)
    user_id = Column(Integer)

    def __init__(
        self,
        guild_id,
        user_id,
    ):
        self.guild_id = guild_id
        self.user_id = user_id


BASE.metadata.create_all(ENGINE)


def get_guild_watcher(guild_id):
    return SESSION.query(Watcher).filter(Watcher.guild_id == str(guild_id)).all()


def add_watcher(guild_id, user_id):
    watcher = (
        SESSION.query(Watcher)
        .filter(Watcher.guild_id == guild_id)
        .filter(Watcher.user_id == user_id)
        .first()
    )
    if watcher is not None:
        return None
    watcher = Watcher(guild_id, user_id)
    SESSION.add(watcher)
    SESSION.commit()
    return True
