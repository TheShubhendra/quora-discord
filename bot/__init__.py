from quora import User
import asyncio


async def runner():
    user = User(username='Saurabh-vishwakarma-228')
    user = await user.profile()
    print(user.followerCount)

asyncio.run(runner())
loop = asyncio.get_event_loop()
loop.run_until_complete()
