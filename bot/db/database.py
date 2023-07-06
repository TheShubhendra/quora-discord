from sqlalchemy import create_engine

from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from typing import Union, Optional, Any

from ..db.schemas import (
    Base,
    User,
)
import sqlalchemy


class DatabaseManager:
    def __init__(self, database_url: str, echo=False) -> None:
        self.db_url = database_url
        self.engine = create_engine(database_url, echo=echo)
        session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_factory)
        self.base = Base

    def getQuoraUsername(self, id: int) -> str | None:
        username = self.session.query(User).filter(User.discord_id == id).first()
        if username:
            username = username.quora_username
        return username

    def addQuoraUsername(
        self,
        discord_id: int,
        quora_username: str,
        discord_username: str,
        follower_count: int,
        access: str = "public",
    ) -> User:
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

    def checkUserExistence(self, discord_id: int) -> bool:
        user = self.session.query(User).filter(User.discord_id == discord_id).first()
        return user

    def removeUserExistence(self, discord_id: int):
        self.session.query(User).filter(User.discord_id == discord_id).delete()
        self.session.commit()

    def update_quoran(
        self,
        discord_id: int,
        username: str,
        followerCount: int,
        access: str = "public",
    ):
        user = self.get_user(discord_id=discord_id)
        user.quora_username = username
        user.access = access
        user.followerCount = followerCount
        self.session.commit()

    def getAllQuorans(self):
        return self.session.query(User).all()
