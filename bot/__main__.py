import json
import discord
from discord.ext import commands
import logging
import asyncio
from pymemcache.client import base
from .bot import QuoraBot

discord.utils.setup_logging()

with open("config.json") as f:
    secrets = json.loads(f.read())

token = secrets["TOKEN"]
MY_GUILD = discord.Object(id=secrets["GUILD"])
# MY_GUILD = discord.Object(id=0)
LOGGING_CHANNEL = discord.Object(id=secrets["LOGGING_CHANNEL"])
DATABASE_URL = secrets["DATABASE_URL"]
REDIS_HOSTNAME = secrets["REDIS_HOSTNAME"]
REDIS_PORT = secrets["REDIS_PORT"]
cache_client = base.Client((REDIS_HOSTNAME, int(REDIS_PORT)))

client = QuoraBot(
    intents=discord.Intents.all(),
    logging=logging,
    LOGGING_GUILD=MY_GUILD,
    database_url=DATABASE_URL,
    logging_channel_id=LOGGING_CHANNEL,
    # cacheManager=cache_client,
)


@client.event
async def on_ready():
    server_name = client.get_guild(client.LOGGING_GUILD.id)
    client.logging.info(
        f"Bot is ready | Exclusive commands are loaded in {server_name.name}({server_name.id})"
    )


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(client.start(token))
except KeyboardInterrupt:
    client.database.close()
    loop.close()
finally:
    loop.close()
