from discord.ext import tasks
from decouple import config
import topgg
from aiohttp import ClientSession
import logging


TOPGG_TOKEN = config("TOPGG_TOKEN")
DBL_TOKEN = config("DBL_TOKEN")

bot.topggpy = topgg.DBLClient(bot, TOPGG_TOKEN)
logger = logging.getLogger(__name__)


@tasks.loop(minutes=30)
async def update_stats():
    """This function runs every 30 minutes to automatically update your server count."""
    try:
        await bot.topggpy.post_guild_count()
        print(f"Posted server count ({bot.topggpy.guild_count})")
    except Exception as e:
        print(f"Failed to post server count\n{e.__class__.__name__}: {e}")
    try:
        async with ClientSession() as session:
            await session.post(
                f"https://discordbotlist.com/api/v1/bots/{bot.client_id}/stats",
                headers={
                    "Authorization": DBL_TOKEN,
                },
                data={
                    "guilds": len(bot.users),
                    "users": len(bot.guilds),
                },
            )
    except Exception as e:
        logger.exception(e)


update_stats.start()
