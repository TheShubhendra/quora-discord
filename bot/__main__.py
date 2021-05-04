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

activity = Streaming(
    name="Quora",
    url="https://quora.com",
)
bot = commands.Bot(
    command_prefix="q!",
    description="Type q!help to get help.",
    activity=activity,
)

for cog in glob.glob("bot/cogs/*.py"):
    bot.load_extension(cog[:-3].replace("/", "."))

bot.run(TOKEN)
