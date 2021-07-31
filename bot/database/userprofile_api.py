from sqlalchemy import (
    Column,
    String,
    Integer,
)

from . import (
    BASE,
    ENGINE,
    SESSION,
)

from decouple import config


CREATE_TABLES = bool(int(config("CREATE_TABLES", 1)))


class Quoran(BASE):
    __tablename__ = "quoran"
    user_id = Column(Integer, primary_key=True)
    discord_id = Column(String(50))
    discord_username = Column(String(100))
    quora_username = Column(String(50))
    access = Column(String(10))

    def __init__(self, discord_id, discord_username, quora_username, access="public"):
        self.discord_id = discord_id
        self.discord_username = discord_username
        self.quora_username = quora_username
        self.access = access


if CREATE_TABLES:
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
    quoran = SESSION.query(Quoran).filter(Quoran.discord_id == str(discord_id)).first()
    SESSION.delete(quoran)
    SESSION.commit()


def update_username(discord_id, username, access="public"):
    user = SESSION.query(Quoran).filter(Quoran.discord_id == str(discord_id)).first()
    user.quora_username = username
    user.access = access
    SESSION.commit()


def add_user(discord_id, discord_username, quora_username, access="public"):
    quoran = Quoran(
        discord_id,
        discord_username,
        quora_username,
        access,
    )
    SESSION.add(quoran)
    SESSION.commit()


def get_quora_username(discord_id):
    quoran = SESSION.query(Quoran).filter(Quoran.discord_id == str(discord_id)).first()
    return quoran.quora_username


def get_user(discord_id=None, user_id=None):
    if discord_id is not None:
        quoran = (
            SESSION.query(Quoran).filter(Quoran.discord_id == str(discord_id)).first()
        )
        return quoran
    if user_id is not None:
        quoran = SESSION.query(Quoran).get(user_id)
        return quoran


def update_access(discord_id, access):
    quoran = SESSION.query(Quoran).filter(Quoran.discord_id == str(discord_id)).first()
    quoran.access = access
    SESSION.commit()


def profile_count():
    return SESSION.query(Quoran).count()
