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

    def __init__(
        self,
        discord_id,
        discord_username,
        quora_username,
    ):
        self.discord_id = discord_id
        self.discord_username = discord_username
        self.quora_username = quora_username


BASE.metadata.create_all(ENGINE)


def does_user_exist(discord_id):
    return (
        SESSION.query(Quoran).filter(Quoran.discord_id == str(discord_id)).first()
        is not None
    )


def delete_user(discord_id):
    quoran = SESSION.query(Quoran).get(str(discord_id))
    SESSION.delete(quoran)
    SESSION.commit()


def add_user(discord_id, discord_username, quora_username):
    if does_user_exist(discord_id):
        delete_user(discord_id)
    quoran = Quoran(
        discord_id,
        discord_username,
        quora_username,
    )
    SESSION.add(quoran)
    SESSION.commit()


def get_quora_username(discord_id):
    quoran = SESSION.query(Quoran).get(str(discord_id))
    return quoran.quora_username
