import discord
from discord.ext import commands
from discord.ext.commands import Bot


class QuoraBot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logging.info("Bot is ready...")


async def setup(bot: Bot) -> None:
    await bot.add_cog(QuoraBot(bot))
