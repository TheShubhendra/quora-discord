from discord.ext import commands
import discord
from ..database import guild_api as gapi
from ..database import watcher_api as wapi
from ..database import userprofile_api as uapi


class Watcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_channel(self, ctx):
        """Set update channel in Server."""
        async with ctx.channel.typing():
            channel = ctx.message.channel_mentions[0]
            gapi.set_update_channel(ctx.guild, channel.id)
            await ctx.reply(
                f"{channel.mention} has been successfully set as an update channel"
            )

    @commands.command()
    async def watch(self, ctx):
        """Add Quora profiles to watching list."""
        async with ctx.channel.typing():
            if not uapi.does_user_exist(ctx.author.id):
                await ctx.repy("Please setup your profile first using `q!setup`.")
                return
            quora_username = uapi.get_quora_username(ctx.author.id)
            update_channel = gapi.get_update_channel(ctx.guild.id)
            if update_channel is None:
                await ctx.reply(
                    "No channel is set update channel in this server.\nPlease ask admin to set the channel using `q!set_channel`."
                )
                return
            wapi.add_watcher(ctx.guild.id, ctx.author.id, quora_username)

            await ctx.reply(
                f"{ctx.author.mention} has been successfully added in watcher list for username {quora_username}"
            )


def setup(bot):
    x = Watcher(bot)
    bot.add_cog(x)
