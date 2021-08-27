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
TOKEN = config("TOKEN")
OWNER_ID = int(config("OWNER_ID", None))
LOGGING = int(config("LOGGING_LEVEL", 20))
LOG_CHANNEL = int(config("LOG_CHANNEL", None))
WATCHER = bool(int(config("WATCHER", 1)))
MC_SERVERS = config("MEMCACHEDCLOUD_SERVERS")
MC_USERNAME = config("MEMCACHEDCLOUD_USERNAME")
MC_PASSWORD = config("MEMCACHEDCLOUD_PASSWORD")
MODERATORS_ID = config("MODERATORS_ID", "0")

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
        await destination.send(
            embed=self.context.bot.embed.command_help(command)
            )


intents = Intents(
    guild_messages=True,
    guilds=True,
    members=True,
)
cache_client = bmemcached.Client(
    MC_SERVERS.split(","),
    MC_USERNAME,
    MC_PASSWORD,
)

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
    log_channel_id=LOG_CHANNEL,
    cache_client=cache_client,
    database_url=DATABASE_URL,
    moderators_id=list(
        map(
            int,
            MODERATORS_ID.split(","),
        )
    ),
)


for cog in glob.glob("bot/cogs/*.py"):
    bot.load_extension(cog[:-3].replace("/", "."))
bot.load_module("/bot/modules/whandler.py", "whandler")
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
