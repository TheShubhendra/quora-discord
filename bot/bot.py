import asyncio
import importlib
import logging
import os
import sys
import time

import bmemcached
import discord
from discord.ext import commands
from discord_components import DiscordComponents
from quora import User
from watcher import Watcher

from .database import DatabaseManager
from .utils.embeds import EmbedBuilder


class QuoraBot(commands.Bot):
    """Custome Class for QuoraBot inherited from `discord.ext.commands.Bot`."""
    def __init__(
        self,
        *args,
        watcher: Watcher = None,
        log_channel_id: int = None,
        cache_client: bmemcached.Client = None,
        database_url: str = None,
        run_watcher: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.watcher = watcher
        self.startTime = time.time()
        self.log_channel_id = log_channel_id
        self.log_channel = None
        self._cache = cache_client
        self.logger = logging.getLogger(__name__)
        self.run_watcher = run_watcher
        self.embed = EmbedBuilder(self)
        self.db = DatabaseManager(database_url, self)

    async def on_command_error(
        self,
        ctx: commands.Context,
        exception: Exception,
    ) -> None:
        self.logger.exception(exception)
        await self.log(exception)
        await ctx.send("Something went wrong.")

    @property
    def up_time(self) -> float:
        return time.time() - self.startTime

    async def load_watcher_data(self):
        self.watcher_list = {}
        for guild in self.guilds:
            guild_watcher = self.db.get_guild_watcher(guild.id)
            for watcher in guild_watcher:
                update_channel = self.db.get_update_channel(guild.id)
                user = self.db.get_user(user_id=watcher.user_id)
                if user.quora_username not in self.watcher_list.keys():
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
                        {
                            "channel_id": update_channel,
                            "discord_id": user.discord_id,
                        }
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

                self.db.update_follower_count(user.user_id, u.followerCount)
                self.db.update_answer_count(user.user_id, u.answerCount)
                self.watcher.add_quora(
                    user.quora_username,
                    update_interval=600,
                    data_dict=data,
                )

    def load_module(
        self,
        file_path: str,
        module_name: str,
    ):
        spec = importlib.util.spec_from_file_location(
            module_name, os.getcwd() + file_path
        )
        module = importlib.util.module_from_spec(spec)
        module.bot = self
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

    def stateCustomizer(
        self,
        answerCount: int,
        followerCount: int,
    ):
        def wrapper(obj):
            obj.answerCount = answerCount
            obj.followerCount = followerCount
            return obj

        return wrapper

    async def on_ready(self):
        DiscordComponents(self)
        await self.inform("Boot up completed.")
        if self.run_watcher:
            await self.load_watcher_data()
            loop = asyncio.get_running_loop()
            loop.create_task(self.watcher.run())
            await self.log(
                f"Boot up completed in {self.up_time} s."
                f"Running{len(self.watcher.updaters)} updaters."
            )

    async def inform(self, information: str):
        admin = await self.fetch_user(self.owner_id)
        await admin.send(information)

    async def log(self, data: str):
        if self.log_channel is None:
            self.log_channel = await self.fetch_channel(self.log_channel_id)
        await self.log_channel.send(f"```\n{data}\n```")
