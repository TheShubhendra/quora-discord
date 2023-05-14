import discord
from discord.ext import commands
from .db.database import DatabaseManager
from sqlalchemy import create_engine
import glob
import os
import bmemcached


class QuoraBot(commands.Bot, DatabaseManager):
    def __init__(
        self,
        intents: discord.Intents,
        logging,
        LOGGING_GUILD=None,
        database_url: str = None,
        logging_channel_id: str = None,
        cacheManager=None,
    ) -> None:
        super().__init__(
            intents=intents, command_prefix="$", activity=discord.Game(name="Quora API")
        )
        self.LOGGING_GUILD = LOGGING_GUILD
        self.database = create_engine(database_url, echo=True).connect()
        self.LOGGING_CHANNEL = logging_channel_id
        self.logging = logging
        self.db: DatabaseManager = DatabaseManager(databaseurl=database_url, echo=False)
        self.cacheManager = bmemcached.Client()

    async def setup_hook(self):
        await self.load_custom_files_extensions(path="bot/cogs")
        self.tree.copy_global_to(guild=self.LOGGING_GUILD)
        await self.tree.sync(guild=self.LOGGING_GUILD)

    async def load_custom_files_extensions(self, path):
        """
        Takes path as an argument and load the extension using client.load_extension
                :param path:
        """
        for files_and_folders in glob.glob(pathname=f"{path}/*"):
            if os.path.isdir(files_and_folders):
                await self.load_custom_files_extensions(path=files_and_folders)
            elif os.path.isfile(files_and_folders) and files_and_folders.endswith(
                ".py"
            ):
                await self.load_extension(files_and_folders.replace("/", ".")[:-3])
