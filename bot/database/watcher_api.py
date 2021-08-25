from . import (
    SESSION,
)

from .tables import Watcher


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
