from discord.ext import commands

INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=838250557805821992&permissions=8&scope=bot"


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Invites bot to your server."""
        await ctx.send(INVITE_LINK)


def setup(bot):
    x = General(bot)
    bot.add_cog(x)
