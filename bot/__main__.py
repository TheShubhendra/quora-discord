import asyncio
import glob
import logging
from typing import Dict

import bmemcached
from decouple import config
from discord import Streaming, Intents, Member
from discord.ext import commands
from watcher import Watcher

from .bot import QuoraBot


DATABASE_URL = config("DATABASE_URL")
REDIS_URL = config("REDIS_URL", None)
TOKEN = config("TOKEN")
OWNER_ID = int(config("OWNER_ID", None))
LOGGING = int(config("LOGGING_LEVEL", 20))
LOG_CHANNEL = config("LOG_CHANNEL", None)
RUN_WATCHER = bool(int(config("RUN_WATCHER", 0)))
# MC_SERVERS = config("MEMCACHEDCLOUD_SERVERS")
# MC_USERNAME = config("MEMCACHEDCLOUD_USERNAME")
# MC_PASSWORD = config("MEMCACHEDCLOUD_PASSWORD")
MODERATORS_ID = config("MODERATORS_ID", "0")
SEND_STATS = bool(int(config("SEND_STATS", 0)))
OWNER_GUILD = config("OWNER_GUILD", None)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=LOGGING,
)

logger = logging.getLogger(__name__)

activity = Streaming(
    name="Quora",
    url="https://quora.com",
)


Mapping = Dict[commands.Cog, list[commands.Command]]


class QuoraHelpCommand(commands.HelpCommand):
    """Custom help command."""

    def __init__(self):
        super().__init__()

    async def send_bot_help(
        self,
        mapping: Mapping,
    ):
        """Method to send help for all commands."""
        embed = self.context.bot.embed.bot_help(mapping)
        await self.context.send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        """Method to send help for a specific command."""
        destination = self.get_destination()
        await destination.send(embed=self.context.bot.embed.command_help(command))


intents = Intents.all()
# cache_client = bmemcached.Client(
#     MC_SERVERS.split(","),
#     MC_USERNAME,
#     MC_PASSWORD,
# )


bot = QuoraBot(
    command_prefix="q!",
    owner_id=OWNER_ID,
    case_insensitive=True,
    strip_after_prefix=True,
    description="This bot lets you to interact with Quora.",
    activity=activity,
    intents=intents,
    help_command=QuoraHelpCommand(),
    watcher=Watcher(),
    log_channel_id=(int(LOG_CHANNEL) if LOG_CHANNEL else None),
    # cache_client=cache_client,
    database_url=DATABASE_URL,
    redis_url=REDIS_URL,
    run_watcher=RUN_WATCHER,
    send_stats=SEND_STATS,
    owner_guild_id = OWNER_GUILD if OWNER_GUILD else None,
    moderators_id=list(
        map(
            int,
            MODERATORS_ID.split(","),
        )
    ),
)



if RUN_WATCHER:
    bot.load_module("/bot/modules/whandler.py", "whandler")
if SEND_STATS:
    bot.load_module("/bot/modules/send_stats.py", "stats_handler")


@bot.listen("on_member_update")
async def update_member(old: Member, new: Member):
    """Listener to update Users's username."""
    logger.info(f"{new} Updated thier profile.")
    user = bot.db.get_user(discord_id=old.id)
    if user is None:
        return
    user.discord_username = f"{new.name}#{str(new.discriminator)}"
    bot.db.session.commit()


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(bot.run(TOKEN))
except KeyboardInterrupt:
    loop.run_until_complete(bot.close())
    bot.watcher.stop()
finally:
    loop.close()
