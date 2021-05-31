from discord.ext import commands
import discord
from ..database import guild_api as api


class Watcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_channel(self, ctx, arg):
        """Set update channel in Server."""
        async with ctx.channel.typing():
            channel = ctx.message.channel_mentions[0]
            api.set_update_channel(ctx.guild, channel.id)
            await ctx.reply(
                f"{channel.mention} has been successfully set as an update channel"
            )


def setup(bot):
    x = Watcher(bot)
    bot.add_cog(x)
