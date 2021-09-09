from sqlalchemy import create_engine

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from typing import Union

from .tables import (
    Base,
    Profile,
    Guild,
    Watcher,
    User,
)


class DatabaseManager:
    def __init__(
        self,
        database_url: str,
        echo=False,
    ):
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=echo)
        session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_factory)
        self.base = Base

    def get_guild(self, guild_id: int):
        return self.session.query(Guild).get(guild_id)

    def get_update_channel(
        self,
        guild_id: int,
    ):
        guild = self.get_guild(guild_id)
        if guild is not None:
            return guild.update_channel
        return None

    def set_update_channel(
        self,
        guild: Guild,
        update_channel: int,
    ):
        _guild = self.get_guild(guild.id)
        if _guild is None:
            _guild = Guild(id=guild.id, name=guild.name, update_channel=update_channel)
            self.session.add(_guild)
        else:
            _guild.update_channel = update_channel
        self.session.commit()

    def does_user_exist(
        self,
        discord_id: int,
        check_hidden: bool = True,
    ):
        if not check_hidden:
            return (
                self.session.query(User)
                .filter(User.discord_id == discord_id)
                .filter(User.access != "none")
                .first()
                is not None
            )
        else:
            return (
                self.session.query(User).filter(User.discord_id == discord_id).first()
                is not None
            )

    def delete_user(
        self,
        discord_id: int,
    ):
        user = self.get_user(discord_id=discord_id)
        self.session.delete_all(quoran.profiles)
        self.session.delete_all(quoran)
        self.session.commit()

    def update_quoran(
        self,
        discord_id: int,
        username: str,
        followerCount: int,
        answerCount: int,
        access: str = "public",
    ):
        user = self.get_user(discord_id=discord_id)
        user.quora_username = username
        user.access = access
        user.followerCount = followerCount
        self.session.commit()

    def add_user(
        self,
        discord_id: int,
        discord_username: str,
        quora_username: str,
        follower_count: int = None,
        access: str = "public",
    ):
        user = User(
            discord_id=discord_id,
            discord_username=discord_username,
            quora_username=quora_username,
            follower_count=follower_count,
            access=access,
        )
        self.session.add(user)
        self.session.commit()
        return user

    def get_quora_username(
        self,
        discord_id: int,
    ):
        user = self.get_user(discord_id=discord_id)
        return user.quora_username

    def get_user(
        self,
        discord_id: int = None,
        user_id: int = None,
    ):
        if discord_id is not None:
            user = (
                self.session.query(User).filter(User.discord_id == discord_id).first()
            )
            return user
        if user_id is not None:
            user = self.session.query(User).get(user_id)
            return user

    def add_profile(
        self,
        user,
        answer_count=None,
        language="en",
    ):
        if isinstance(user, User):
            if not any([p.language==language for p in user.profiles]):
                user.profiles.append(
                    Profile(
                        language=language,
                        answer_count=answer_count,
                        )
                    )
            else:
                raise Exception("Profile already linked on this language")
        elif isinstance(user, int):
            self.session.add(
                Profile(
                    user_id=user,
                    language=language,
                    )
                )
        self.session.commit()

    def update_access(
        self,
        discord_id: int,
        access: str,
    ):
        user = self.get_user(discord_id=discord_id)
        quoran.access = access
        self.session.commit()

    def profile_count(self):
        return self.session.query(User).count()

    def update_answer_count(
        self,
        user_id: int,
        countChange: int,
        language="en",
    ):
        user = self.session.query(User).get(user_id)
        account = (
            self.session.query(Profile)
            .filter(Profile.user_id == user_id)
            .filter(Profile.language == language)
        )
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
        account = self.get_user(user_id=user_id)
        if account.follower_count is None:
            account.follower_count = 0
        account.follower_count += countChange
        self.session.commit()

    def get_guild_watcher(self, guild_id: int):
        return self.session.query(Watcher).filter(Watcher.guild_id == guild_id).all()

    def add_watcher(
        self,
        guild_id: int,
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
