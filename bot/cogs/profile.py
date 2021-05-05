from discord.ext import commands
from quora import User
from bot.database import userprofile_api as api
from bot.utils import (
    extract_quora_username,
    profile_embed,
)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setprofile(self, ctx, quora_username_or_profile_link):
        """Links your Quora profile."""
        username = extract_quora_username(quora_username_or_profile_link)
        if username is None:
            await ctx.reply("Username or profile link is not valid")
            return
        try:
            api.add_user(
                ctx.author.id,
                ctx.author.name,
                username,
            )
            await ctx.reply(
                f"Your username {username} has been successfully updated in the database."
            )
        except:
            await ctx.reply("An unknown error occurred.")

    @commands.command()
    async def profile(self, ctx, quora_username):
        """Gives details of any Quora profile."""
        user = User(quora_username)
        profile = await user.profile()
        await ctx.send(embed=profile_embed(profile))


def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
