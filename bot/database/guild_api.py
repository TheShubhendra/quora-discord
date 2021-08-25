from . import (
    SESSION,
)

from .tables import Guild


def get_guild(guild_id):
    return SESSION.query(Guild).get(str(guild_id))


def get_update_channel(guild_id):
    guild = get_guild(guild_id)
    if guild is not None:
        return guild.update_channel
    return None


def set_update_channel(guild, update_channel):
    _guild = get_guild(guild.id)
    if _guild is None:
        _guild = Guild(guild.id, guild.name, update_channel)
        SESSION.add(_guild)
    else:
        _guild.update_channel = update_channel
    SESSION.commit()
