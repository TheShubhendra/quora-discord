from sqlalchemy import (
    Column,
    String,
)

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
    return SESSION.query(Watcher).get(str(guild_id)).all()


def add_watcher(guild_id, user_id, quora_username):
    watcher = Watcher(guild_id, user_id)
    SESSION.add(watcher)
    SESSION.commit()
