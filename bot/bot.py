import asyncio
import importlib
import logging
import os
import sys
from typing import (
    List,
    Union,
)
import time

from aiohttp import ClientSession
import bmemcached
import discord
from discord.ext import commands
from discord_components import DiscordComponents
from quora import User
from watcher import Watcher

from .database import DatabaseManager
from .mixins import WatcherMixin, ObjectFactory
from .utils.embeds import EmbedBuilder


class QuoraBot(commands.Bot, WatcherMixin, ObjectFactory):
    """Custome Class for QuoraBot inherited from `discord.ext.commands.Bot`."""

    def __init__(
        self,
        *args,
        watcher: Watcher = None,
        log_channel_id: int = None,
        cache_client: bmemcached.Client = None,
        database_url: str = None,
        run_watcher: bool = True,
        send_stats: bool = True,
        moderators_id: List[int] = [],
        session: ClientSession = None,
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
        self.db = DatabaseManager(database_url)
        self.moderators_id = moderators_id
        self._session = session
        self.send_stats = send_stats

    async def on_command_error(
        self,
        ctx: commands.Context,
        exception: Exception,
    ) -> None:
        self.logger.exception(exception)
        await self.log(
            f"""
{exception}
channel: {ctx.channel.id} {ctx.channel.name}
guild: {ctx.guild.id} {ctx.guild.name}
author: {ctx.author.id} {ctx.author.name+ctx.author.discriminator}
command: {ctx.message.id} {ctx.message.content}
"""
        )
        await ctx.send(exception)

    @property
    def up_time(self) -> float:
        return time.time() - self.startTime

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

    def is_moderator(self, member: Union[int, discord.Member]):
        if isinstance(member, discord.Member):
            member = member.id
        return member in self.moderators_id or member == self.owner_id

    def is_admin(self, member: Union[int, discord.Member]):
        if isinstance(member, discord.Member):
            member = member.id
        return member == self.owner_id
