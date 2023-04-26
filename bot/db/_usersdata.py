from quora import User
import asyncio
from typing import Dict, Tuple, Callable, List, Any, Coroutine
from quora import Topic


async def getQuoraUserData(username: str) -> Tuple[Callable,
                                                   List,
                                                   Coroutine[Any, Any, list[Topic]]]:
    """Get user data from the database if user exists else parse it

    Args:
        username (str): provide quora username

    Returns:
        Tuple[Callable,List[Callable,Callable, Callable],Coroutine[Any, Any, list[Topic]]]
    """
    user = User(username=username)
    profile = await user.profile()
    answers = await user.answers()
    topic = await user.knows_about()
    return profile, answers, topic
