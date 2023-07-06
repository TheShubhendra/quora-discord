import asyncio
import logging
import os

import discord

from .bot import QuoraBot

discord.utils.setup_logging()

TOKEN = os.environ["TOKEN"]
MY_GUILD = discord.Object(id=int(os.environ["GUILD"]))
LOGGING_CHANNEL = discord.Object(id=int(os.environ["LOGGING_CHANNEL"]))
DATABASE_URL = os.environ["DATABASE_URL"]


client = QuoraBot(
    intents=discord.Intents.all(),
    logging=logging,
    LOGGING_GUILD=MY_GUILD,
    database_url=DATABASE_URL,
    logging_channel_id=LOGGING_CHANNEL,
)


@client.event
async def on_ready():
    server_name = client.get_guild(client.LOGGING_GUILD.id)
    client.logging.info(
        f"Bot is ready | Exclusive commands are loaded\
         in {server_name.name}({server_name.id})"
    )


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(client.start(TOKEN))
except KeyboardInterrupt:
    client.database.close()
    loop.close()
finally:
    loop.close()
