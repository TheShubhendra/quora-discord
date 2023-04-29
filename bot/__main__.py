import glob
import json
import discord
from discord.ext import commands
import pathlib
from sqlalchemy import create_engine
import os
import logging
import asyncio
from .db.database import DatabaseManager


discord.utils.setup_logging()

with open('config.json') as f:
    secrets = json.loads(f.read())

token = secrets['TOKEN']
MY_GUILD = discord.Object(id=secrets['GUILD'])
# MY_GUILD = discord.Object(id=0)
LOGGING_CHANNEL = discord.Object(id=secrets['LOGGING_CHANNEL'])
DATABASE_URL = secrets['DATABASE_URL']


class MyClient(commands.Bot, DatabaseManager):
    def __init__(self,
                 intents: discord.Intents,
                 logging,
                 LOGGING_GUILD=None,
                 database_url: str = None,
                 logging_channel_id: str = None,
                 ) -> None:

        super().__init__(intents=intents,
                         command_prefix='$',
                         activity=discord.Game(name="Quora API"))
        self.LOGGING_GUILD = LOGGING_GUILD
        self.database_url = database_url
        self.database = create_engine(self.database_url, echo=True).connect()
        self.LOGGING_CHANNEL = logging_channel_id
        self.logging = logging
        self.db: DatabaseManager = DatabaseManager(
            databaseurl=self.database_url, echo=False)

    async def setup_hook(self):
        await self.load_extension('bot.bot')
        await self.load_custom_files_extensions(path='bot/cogs')
        self.tree.copy_global_to(guild=self.LOGGING_GUILD)
        await self.tree.sync(guild=self.LOGGING_GUILD)

    async def load_custom_files_extensions(self, path):
        """
Takes path as an argument and load the extension using client.load_extension
        :param path:
        """
        for files_and_folders in glob.glob(pathname=f'{path}/*'):
            if os.path.isdir(files_and_folders):
                await self.load_custom_files_extensions(path=files_and_folders)
            elif os.path.isfile(files_and_folders) and files_and_folders.endswith('.py'):
                await self.load_extension(files_and_folders.replace('/', '.')[:-3])


print(MY_GUILD.id)
client = MyClient(
    intents=discord.Intents.all(),
    logging=logging,
    LOGGING_GUILD=MY_GUILD,
    database_url=DATABASE_URL,
    logging_channel_id=LOGGING_CHANNEL
)


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(client.start(token))
except KeyboardInterrupt:
    client.database.close()
    loop.close()
finally:
    loop.close()
