from discord.ext import tasks
from decouple import config
import topgg

dbl_token = config ("TOPGG_TOKEN")
bot.topggpy = topgg.DBLClient(bot, dbl_token)

@tasks.loop(minutes=30)
async def update_stats():
    """This function runs every 30 minutes to automatically update your server count."""
    try:
        await bot.topggpy.post_guild_count()
        print(f"Posted server count ({bot.topggpy.guild_count})")
    except Exception as e:
        print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

update_stats.start()
