from . import (
    SESSION,
)

from .tables import Quoran


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


def update_quoran(discord_id, username, followerCount, answerCount, access="public"):
    user = SESSION.query(Quoran).filter(Quoran.discord_id == str(discord_id)).first()
    user.quora_username = username
    user.access = access
    user.followerCount = followerCount
    user.answerCount = answerCount
    SESSION.commit()


def add_user(
    discord_id,
    discord_username,
    quora_username,
    follower_count=None,
    answer_count=None,
    access="public",
):
    quoran = Quoran(
        discord_id,
        discord_username,
        quora_username,
        follower_count,
        answer_count,
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


def update_answer_count(user_id, countChange):
    account = SESSION.query(Quoran).get(user_id)
    if account.answer_count is None:
        account.answer_count = countChange
    else:
        account.answer_count += countChange
    SESSION.commit()


def update_follower_count(user_id, countChange):
    account = SESSION.query(Quoran).get(user_id)
    if account.follower_count is None:
        account.follower_count = 0
    account.follower_count += countChange
    SESSION.commit()
