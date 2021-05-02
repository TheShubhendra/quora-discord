from discord.ext import commands
from decouple import config
import logging
import glob

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
)
TOKEN = config("TOKEN")
bot = commands.Bot(command_prefix="q!")

for cog in glob.glob("bot/cogs/*.py"):
    bot.load_extension(cog[:-3].replace("/", "."))

bot.run(TOKEN)
