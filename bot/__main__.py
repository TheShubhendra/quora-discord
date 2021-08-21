from discord.ext import commands
from discord import Streaming, Intents
from decouple import config
import logging
import glob
import time
import asyncio
import sys
import os
import importlib
from .utils.embeds import (
    bot_help_embed,
    command_help_embed,
)
from watcher import Watcher
from .database import watcher_api as wapi
from .database import userprofile_api as uapi
from .database import guild_api as gapi
from .database import SESSION

from quora.sync import User
from discord_components import DiscordComponents
import bmemcached

TOKEN = config("TOKEN")
OWNER_ID = int(config("OWNER_ID", None))
LOGGING = int(config("LOGGING_LEVEL", 20))
LOG_CHANNEL = int(config("LOG_CHANNEL", None))
WATCHER = bool(int(config("WATCHER", 1)))
MC_SERVERS = config("MEMCACHEDCLOUD_SERVERS")
MC_USERNAME = config("MEMCACHEDCLOUD_USERNAME")
MC_PASSWORD = config("MEMCACHEDCLOUD_PASSWORD")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=LOGGING,
)

logger = logging.getLogger(__name__)

activity = Streaming(
    name="Quora",
    url="https://quora.com",
)


class QuoraHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = bot_help_embed(mapping)
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        destination = self.get_destination()
        await destination.send(embed=command_help_embed(command))


class QuoraBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.watcher = Watcher()
        self.startTime = time.time()
        self.log_channel_id = LOG_CHANNEL
        self.log_channel = None
        self._cache = bmemcached.Client(
            MC_SERVERS.split(","),
            MC_USERNAME,
            MC_PASSWORD,
        )
        self.logger = logging.getLogger("Bot")

    async def on_command_error(self, ctx, exception):
        self.logger.exception(exception)
        await self.log(exception)
        await self.log(sys.exc_info())
        await ctx.send("Something went wrong.")

    def up_time(self):
        return time.time() - self.startTime

    async def load_watcher_data(self):
        self.watcher_list = {}
        for guild in self.guilds:
            guild_watcher = wapi.get_guild_watcher(guild.id)
            for watcher in guild_watcher:
                update_channel = gapi.get_update_channel(guild.id)
                user = uapi.get_user(user_id=watcher.user_id)
                if not user.quora_username in self.watcher_list.keys():
                    data_dict = {
                        "user_id": user.user_id,
                        "dispatch_to": [
                            {
                                "channel_id": update_channel,
                                "discord_id": user.discord_id,
                            }
                        ],
                    }
                    self.watcher_list[user] = data_dict
                else:
                    data = self.watcher_list[user.quora_username]
                    ls = data["dispatch_to"]
                    ls.append(
                        {"channel_id": update_channel, "discord_id": user.discord_id}
                    )
                    data["dispatch_to"] = ls
                    self.watcher_list[user.quora_username] = data
        for user, data in self.watcher_list.items():
            if user.answer_count and user.follower_count:
                self.watcher.add_quora(
                    user.quora_username,
                    update_interval=900,
                    data_dict=data,
                    stateInitializer=self.stateCustomizer(
                        user.answer_count, user.follower_count
                    ),
                )
            else:
                u = User(user.quora_username)
                u = await u.profile()

                uapi.update_follower_count(user.user_id, u.followerCount)
                uapi.update_answer_count(user.user_id, u.answerCount)
                self.watcher.add_quora(
                    user.quora_username,
                    update_interval=600,
                    data_dict=data,
                )

    def load_module(self, file_path, module_name):
        spec = importlib.util.spec_from_file_location(
            module_name, os.getcwd() + file_path
        )
        module = importlib.util.module_from_spec(spec)
        module.bot = self
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

    def stateCustomizer(self, answerCount, followerCount):
        def wrapper(obj):
            obj.answerCount = answerCount
            obj.followerCount = followerCount
            return obj

        return wrapper

    async def on_ready(self):
        DiscordComponents(self)
        await self.inform("Boot up completed.")
        if WATCHER:
            await self.load_watcher_data()
            loop = asyncio.get_running_loop()
            loop.create_task(self.watcher.run())
            await self.log(
                f"Boot up completed in {self.up_time()} s.\nRunning {len(self.watcher.updaters)} updaters."
            )

    async def inform(self, information):
        admin = await self.fetch_user(self.owner_id)
        await admin.send(information)

    async def log(self, data):
        if self.log_channel is None:
            self.log_channel = await self.fetch_channel(self.log_channel_id)
        await self.log_channel.send(f"```\n{data}\n```")

    async def on_member_remove(self, member):
        logger.info("Someone left")
        if member.id == bot.owner_id:
            guild = member.guild
            await guild.system_channel.send(
                "My Developer Shubhendra Sir left the Server so I'm leaving too. Don't expect me back."
            )
            print("Going to leave", str(guild), guild.id)
            await guild.leave()

intents = Intents(
    guild_messages=True,
    guilds=True,
    members=True,
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
)


for cog in glob.glob("bot/cogs/*.py"):
    bot.load_extension(cog[:-3].replace("/", "."))
bot.load_module("/bot/modules/whandler.py", "whandler")
bot.load_module("/bot/modules/send_stats.py", "stats_handler")


@bot.listen("on_member_update")
async def update_member(old, new):
    logger.info(f"{new} Updated thier profile.")
    user = uapi.get_user(discord_id=old.id)
    if user is None:
        return
    user.discord_username = f"{new.name}#{str(new.discriminator)}"
    SESSION.commit()


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(bot.run(TOKEN))
except KeyboardInterrupt:
    loop.run_until_complete(bot.close())
    bot.watcher.stop()
finally:
    loop.close()
