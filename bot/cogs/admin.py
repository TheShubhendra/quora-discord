from discord.ext import commands
from discord import File
from decouple import config
import heroku3
import asyncio
import os

HEROKU_API_KEY = config("HEROKU_API_KEY",None)
HEROKU_APP_NAME = config("HEROKU_APP_NAME", None)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        aliases=["l","log"],
        hidden=True,
        )
    async def logs(self, ctx):
        if ctx.author.id != self.bot.owner_id:
            await ctx.send("You don't have permission to execute this command.")
            return
        await ctx.trigger_typing()
        client = heroku3.from_key(HEROKU_API_KEY)
        app = client.app(HEROKU_APP_NAME)
        logs = app.get_log()
        if len(logs)>1000:
            with open("logs.txt", "w") as log:
                log.write(logs)
            with open("logs.txt", "rb") as log:
                await ctx.send(file=File(log, filename="Heroku logs"), delete_after=60)
        else:
            await ctx.send(logs, delete_after=60)
        await asyncio.sleep(3)
        os.remove("logs.txt")


def setup(bot):
    cog = Admin(bot)
    bot.add_cog(cog)
