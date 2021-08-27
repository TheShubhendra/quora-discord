from discord.ext import commands
from discord import File
from decouple import config
import heroku3
import asyncio
import os

HEROKU_API_KEY = config("HEROKU_API_KEY", None)
HEROKU_APP_NAME = config("HEROKU_APP_NAME", None)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["l", "log"],
        hidden=True,
    )
    async def logs(self, ctx: commands.Context):
        await ctx.trigger_typing()
        client = heroku3.from_key(HEROKU_API_KEY)
        app = client.app(HEROKU_APP_NAME)
        logs = app.get_log()
        if len(logs) > 1000:
            with open("logs.txt", "w") as log:
                log.write(logs)
            with open("logs.txt", "rb") as log:
                await ctx.send(
                    file=File(log, filename="Heroku logs"),
                    delete_after=60,
                    )
        else:
            await ctx.send(logs, delete_after=60)
        await asyncio.sleep(3)
        os.remove("logs.txt")

    @commands.command(hidden=True)
    async def setp(self, ctx: commands.Context, arg1: str, arg2: str):
        cog = self.bot.get_cog("Profile")
        user = ctx.message.mentions[0]
        await cog.setprofile(ctx, arg2, user=user)

    @commands.command(hidden=True)
    async def guilds(self, ctx: commands.Context):
        guilds = self.bot.guilds
        txt = "```\n"
        for i in guilds:
            txt += f"{i.id}  : {i}\n"
        await ctx.reply(txt + "```", delete_after=30)

    async def cog_check(self, ctx: commands.Context):
        if ctx.bot.is_moderator(ctx.author):
            return True
        else:
            await ctx.reply(
                "This command can be used by owner or a bot moderator only."
            )
            return False


def setup(bot):
    cog = Admin(bot)
    bot.add_cog(cog)
