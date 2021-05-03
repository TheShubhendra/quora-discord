from discord.ext import commands
from profiles.quora import User
from bot.database import userprofile_api as api
from bot.utils.parser import extract_quora_username


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setprofile(self, ctx, arg):
        username = extract_quora_username(arg)
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
    async def profile(self, ctx, arg):
        await ctx.send(User(arg))


def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
