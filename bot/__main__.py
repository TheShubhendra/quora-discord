from discord.ext import commands
from discord import Streaming
from decouple import config
import logging
import glob

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
)

TOKEN = config("TOKEN")
OWNER_ID = config("OWNER_ID", None)
activity = Streaming(
    name="Quora",
    url="https://quora.com",
)
bot = commands.Bot(
    command_prefix="q!",
    owner_id=OWNER_ID,
    strip_after_prefix=True,
    description="This bot lets you to interact with Quora.",
    activity=activity,
)

for cog in glob.glob("bot/cogs/*.py"):
    bot.load_extension(cog[:-3].replace("/", "."))

bot.run(TOKEN)
