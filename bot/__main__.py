# from sqlalchemy import create_engine
# from sqlalchemy import text
# engine = create_engine(
#     "postgresql+psycopg2://postgres:saurabh@localhost/mydb")
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * from actor"))
import glob
import json
import discord
from discord.ext import commands
import pathlib
from sqlalchemy import create_engine
import os
import logging
import asyncio


discord.utils.setup_logging()

with open('config.json') as f:
    secrets = json.loads(f.read())

token = secrets['TOKEN']
MY_GUILD = discord.Object(id=secrets['GUILD'])
LOGGING_CHANNEL = discord.Object(id=secrets['LOGGING_CHANNEL'])
DATABASE_URL = secrets['DATABASE_URL']


class MyClient(commands.Bot):
    def __init__(self,
                 intents: discord.Intents,
                 logging,
                 testing_guild=None,
                 database_url: str = None,
                 logging_channel_id: str = None,
                 ) -> None:

        super().__init__(intents=intents,
                         command_prefix='$',
                         activity=discord.Game(name="Quora API"))
        self.testing_guild = testing_guild
        self.database_url = database_url
        self.database = create_engine(self.database_url, echo=True).connect()
        self.logging_channel_id = logging_channel_id
        self.logging = logging

    async def setup_hook(self):
        await self.load_extension('bot.bot')
        await self.load_custom_files_extensions(path='bot/cogs')
        self.tree.copy_global_to(guild=self.testing_guild)
        await self.tree.sync(guild=self.testing_guild)

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


client = MyClient(
    intents=discord.Intents.all(),
    logging=logging,
    testing_guild=MY_GUILD,
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
