from sqlalchemy import create_engine

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from typing import Union

from .tables import (
    Base,
    Guild,
    Quoran,
    Watcher,
)


class DatabaseManager:
    def __init__(
        self,
        database_url: str,
        bot: "QuoraBot",
        echo=False,
    ):
        self.database_url = database_url
        self.bot = bot
        self.engine = create_engine(database_url, echo=echo)
        session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_factory)
        self.base = Base

    def get_guild(self, guild_id: Union[int, str]):
        return self.session.query(Guild).get(str(guild_id))

    def get_update_channel(
        self,
        guild_id: Union[int, str],
    ):
        guild = self.get_guild(guild_id)
        if guild is not None:
            return guild.update_channel
        return None

    def set_update_channel(
        self,
        guild: Guild,
        update_channel: Union[int, str],
    ):
        _guild = self.get_guild(guild.id)
        if _guild is None:
            _guild = Guild(guild.id, guild.name, update_channel)
            self.session.add(_guild)
        else:
            _guild.update_channel = update_channel
        self.session.commit()

    def does_user_exist(
        self,
        discord_id: Union[int, str],
        check_hidden: bool = False,
    ):
        if not check_hidden:
            return (
                self.session.query(Quoran)
                .filter(Quoran.discord_id == str(discord_id))
                .filter(Quoran.access != "none")
                .first()
                is not None
            )
        else:
            return (
                self.session.query(Quoran)
                .filter(Quoran.discord_id == str(discord_id))
                .first()
                is not None
            )

    def delete_user(
        self,
        discord_id: Union[int, str],
    ):
        quoran = (
            self.session.query(Quoran)
            .filter(Quoran.discord_id == str(discord_id))
            .first()
        )
        self.session.delete(quoran)
        self.session.commit()

    def update_quoran(
        self,
        discord_id: Union[int, str],
        username: str,
        followerCount: int,
        answerCount: int,
        access: str = "public",
    ):
        user = (
            self.session.query(Quoran)
            .filter(Quoran.discord_id == str(discord_id))
            .first()
        )
        user.quora_username = username
        user.access = access
        user.followerCount = followerCount
        user.answerCount = answerCount
        self.session.commit()

    def add_user(
        self,
        discord_id: Union[int, str],
        discord_username: str,
        quora_username: str,
        follower_count: int = None,
        answer_count: int = None,
        access: str = "public",
    ):
        quoran = Quoran(
            discord_id,
            discord_username,
            quora_username,
            follower_count,
            answer_count,
            access,
        )
        self.session.add(quoran)
        self.session.commit()

    def get_quora_username(
        self,
        discord_id: Union[int, str],
    ):
        quoran = (
            self.session.query(Quoran)
            .filter(Quoran.discord_id == str(discord_id))
            .first()
        )
        return quoran.quora_username

    def get_user(
        self,
        discord_id: Union[int, str] = None,
        user_id: int = None,
    ):
        if discord_id is not None:
            quoran = (
                self.session.query(Quoran)
                .filter(Quoran.discord_id == str(discord_id))
                .first()
            )
            return quoran
        if user_id is not None:
            quoran = self.session.query(Quoran).get(user_id)
            return quoran

    def update_access(
        self,
        discord_id: Union[int, str],
        access: str,
    ):
        quoran = (
            self.session.query(Quoran)
            .filter(Quoran.discord_id == str(discord_id))
            .first()
        )
        quoran.access = access
        self.session.commit()

    def profile_count(self):
        return self.session.query(Quoran).count()

    def update_answer_count(
        self,
        user_id: int,
        countChange: int,
    ):
        account = self.session.query(Quoran).get(user_id)
        if account.answer_count is None:
            account.answer_count = countChange
        else:
            account.answer_count += countChange
        self.session.commit()

    def update_follower_count(
        self,
        user_id: int,
        countChange: int,
    ):
        account = self.session.query(Quoran).get(user_id)
        if account.follower_count is None:
            account.follower_count = 0
        account.follower_count += countChange
        self.session.commit()

    def get_guild_watcher(self, guild_id: Union[int, str]):
        return (
            self.session.query(Watcher).filter(Watcher.guild_id == str(guild_id)).all()
        )

    def add_watcher(
        self,
        guild_id: Union[int, str],
        user_id: int,
    ):
        watcher = (
            self.session.query(Watcher)
            .filter(Watcher.guild_id == guild_id)
            .filter(Watcher.user_id == user_id)
            .first()
        )
        if watcher is not None:
            return None
        watcher = Watcher(guild_id, user_id)
        self.session.add(watcher)
        self.session.commit()
        return True
