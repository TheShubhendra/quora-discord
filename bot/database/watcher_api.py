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
    guild_name = Column(String(50), primary_key=True)
    discord_username = Column(String(50))
    quora_username = Column(String(50))

    def __init__(
        self,
        guild_id,
        discord_username,
        quora_username,
    ):
        self.guild_id = guild_id
        self.discord_username = discord_username
        self.quora_username = quora_username


BASE.metadata.create_all(ENGINE)


def get_guild_watcher(guild_id):
    return SESSION.query(Watcher).get(str(guild_id))


def add_watcher(guild_id, discord_username, quora_username):
    watcher = Watcher(guild_name, discord_username, quora_username)
    SESSION.add(watcher)
    SESSION.commit()
