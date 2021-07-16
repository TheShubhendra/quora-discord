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
OWNER_ID = int(config("OWNER_ID", None))
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


@bot.listen()
async def on_member_remove(member):
    print("XXXXXXXXXXXXXXXXXX")
    if member.id == bot.owner_id:
        guild = member.guild
        await guild.system_channel.send(
            "My Developer Shubhendra Sir left the Server so I'm leaving too. Don't expect me back."
        )
        print("Going to leave", str(guild), guild.id)
        await guild.leave()


for cog in glob.glob("bot/cogs/*.py"):
    bot.load_extension(cog[:-3].replace("/", "."))

bot.run(TOKEN)
