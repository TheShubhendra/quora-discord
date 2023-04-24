from quora import User
import asyncio
from typing import Dict


async def getQuoraUserData(username: str) -> Dict[str, str]:
    profile = User(username=username)
    user = await profile.profile()
    return user
