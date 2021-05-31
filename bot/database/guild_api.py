from sqlalchemy import (
    Column,
    String,
)

from . import (
    BASE,
    ENGINE,
    SESSION,
)


class Guild(BASE):
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


BASE.metadata.create_all(ENGINE)


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
