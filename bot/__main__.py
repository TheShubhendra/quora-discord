from discord.ext import commands
from discord import Streaming
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


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
)

TOKEN = config("TOKEN")
OWNER_ID = int(config("OWNER_ID", None))


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

    async def on_command_error(self, ctx, exception):
        await ctx.send(exception)

    def up_time(self):
        return time.time() - self.startTime

    def load_watcher_data(self):
        self.watcher_list = {}
        for guild in self.guilds:
            guild_watcher = wapi.get_guild_watcher(guild.id)
            for watcher in guild_watcher:
                update_channel = gapi.get_update_channel(guild.id)
                user = uapi.get_user(user_id=watcher.user_id)
                if not user.quora_username in self.watcher_list.keys():
                    data_dict = {
                        "dispatch_to": [
                            {
                                "channel_id": update_channel,
                                "discord_id": user.discord_id,
                            }
                        ]
                    }
                    self.watcher_list[user.quora_username] = data_dict
                else:
                    data = self.watcher_list[user.quora_username]
                    ls = data["dispatch_to"]
                    ls.append(
                        {"channel_id": update_channel, "discord_id": user.discord_id}
                    )
                    data["dispatch_to"] = ls
                    self.watcher_list[user.quora_username] = data
        for i, j in self.watcher_list.items():
            self.watcher.add_quora(
                i,
                update_interval=60,
                data_dict=j,
            )

    def load_module(self, file_path, module_name):
        spec = importlib.util.spec_from_file_location(
            module_name, os.getcwd() + file_path
        )
        module = importlib.util.module_from_spec(spec)
        module.bot = self
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

    async def on_ready(self):
        self.load_watcher_data()
        loop = asyncio.get_running_loop()
        loop.create_task(self.watcher.run())


bot = QuoraBot(
    command_prefix="q!",
    owner_id=OWNER_ID,
    strip_after_prefix=True,
    description="This bot lets you to interact with Quora.",
    activity=activity,
    help_command=QuoraHelpCommand(),
)


@bot.listen()
async def on_member_remove(member):
    print("XXXXXXXXXXXXXXXXXX")
    if member.id == bot.owner_id:
        guild = member.guild
        await guild.system_channel.send(
            "My Developer Shubhendra Sir left the Server so I'm leaving too. Don't expect me back."
        )
        print("Going to leave", str(guild), guild.id)
        await guild.leave()


for cog in glob.glob("bot/cogs/*.py"):
    bot.load_extension(cog[:-3].replace("/", "."))
bot.load_module("/bot/modules/whandler.py", "whandler")

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(bot.run(TOKEN))
except KeyboardInterrupt:
    loop.run_until_complete(bot.close())
    bot.watcher.stop()
finally:
    loop.close()
