from discord.ext import commands
import discord
from ..database import guild_api as api
from ..database import watcher_api as wapi


class Watcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_channel(self, ctx):
        """Set update channel in Server."""
        async with ctx.channel.typing():
            channel = ctx.message.channel_mentions[0]
            api.set_update_channel(ctx.guild, channel.id)
            await ctx.reply(
                f"{channel.mention} has been successfully set as an update channel"
            )

    @commands.command()
    async def watch(self, ctx, quora_username):
        """Add Quora profiles to watching list."""
        async with ctx.channel.typing():
            wapi.add_watcher(ctx.guild.id, ctx.author.id, quora_username)
            await ctx.reply(
                f"{ctx.author.mention} has been successfully added in watcher list for username {quora_username}"
            )


def setup(bot):
    x = Watcher(bot)
    bot.add_cog(x)
