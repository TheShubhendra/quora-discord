from discord.ext import commands
from discord import Streaming
from decouple import config
import logging
import glob
from .utils.embeds import (
    bot_help_embed,
    command_help_embed,
)

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


class QuoraHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = bot_help_embed(mapping)
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        destination = self.get_destination()
        await destination.send(embed=command_help_embed(command))


class QuoraBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_command_error(self, ctx, exception):
        await ctx.send(exception)


bot = QuoraBot(
    command_prefix="q!",
    owner_id=OWNER_ID,
    strip_after_prefix=True,
    description="This bot lets you to interact with Quora.",
    activity=activity,
    help_command=QuoraHelpCommand(),
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
