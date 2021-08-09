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
            if not ctx.author.guild_permissions.administrator:
                await ctx.reply("Only Admins can execute this command.")
                return
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
                await ctx.reply("Please setup your profile first using `q!setup`.")
                return
            user = uapi.get_user(discord_id=ctx.author.id)
            update_channel = gapi.get_update_channel(ctx.guild.id)
            if update_channel is None:
                await ctx.reply(
                    "No channel is set update channel in this server.\nPlease ask admin to set the channel using `q!set_channel`."
                )
                return
            if wapi.add_watcher(str(ctx.guild.id), user.user_id) is None:
                await ctx.reply(
                    f"You are alreay watching {user.quora_username} on this server."
                )
                return
            self.bot.watcher.add_quora(
                user.quora_username,
                update_interval=60,
                data_dict={
                    "dispatch_to": [
                        {
                            "channel_id": update_channel,
                            "discord_id": user.discord_id,
                        }
                    ],
                },
            )
            await ctx.reply(
                f"{ctx.author.mention} has been successfully added in watcher list for username {user.quora_username}"
            )


def setup(bot):
    x = Watcher(bot)
    bot.add_cog(x)
