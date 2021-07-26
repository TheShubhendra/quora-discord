from sqlalchemy import (
    Column,
    String,
)

from . import (
    BASE,
    ENGINE,
    SESSION,
)


class Quoran(BASE):
    __tablename__ = "quoran"
    discord_id = Column(String(50), primary_key=True)
    discord_username = Column(String(100))
    quora_username = Column(String(50))
    access = Column(String(10))

    def __init__(self, discord_id, discord_username, quora_username, access=None):
        self.discord_id = discord_id
        self.discord_username = discord_username
        self.quora_username = quora_username
        if access is None:
            access = "public"
        self.access = access


BASE.metadata.create_all(ENGINE)


def does_user_exist(discord_id, check_hidden=False):
    if not check_hidden:
        return (
            SESSION.query(Quoran)
            .filter(Quoran.discord_id == str(discord_id))
            .filter(Quoran.access != "none")
            .first()
            is not None
        )
    else:
        return (
            SESSION.query(Quoran).filter(Quoran.discord_id == str(discord_id)).first()
            is not None
        )


def delete_user(discord_id):
    quoran = SESSION.query(Quoran).get(str(discord_id))
    SESSION.delete(quoran)
    SESSION.commit()


def add_user(discord_id, discord_username, quora_username, access=None):
    if does_user_exist(discord_id, check_hidden=True):
        delete_user(discord_id)
    if access is None:
        access = "public"
    quoran = Quoran(
        discord_id,
        discord_username,
        quora_username,
        access,
    )
    SESSION.add(quoran)
    SESSION.commit()


def get_quora_username(discord_id):
    quoran = SESSION.query(Quoran).get(str(discord_id))
    return quoran.quora_username


def update_access(discord_id, access):
    quoran = SESSION.query(Quoran).get(str(discord_id))
    quoran.access = access
    SESSION.commit()
