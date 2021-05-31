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
    user_id = Column(String(50))
    quora_username = Column(String(50))

    def __init__(
        self,
        guild_id,
        user_id,
        quora_username,
    ):
        self.guild_id = guild_id
        self.user_id = user_id
        self.quora_username = quora_username


BASE.metadata.create_all(ENGINE)


def get_guild_watcher(guild_id):
    return SESSION.query(Watcher).get(str(guild_id))


def add_watcher(guild_id, user_id, quora_username):
    watcher = Watcher(guild_id, user_id, quora_username)
    SESSION.add(watcher)
    SESSION.commit()
