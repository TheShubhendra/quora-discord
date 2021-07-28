import asyncio
from discord.ext import commands
import discord
from bot.utils import dev_embed, Embed, stats_embed, count_file_and_lines as count
from bot.database import userprofile_api as api


BOT_INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=838250557805821992&permissions=2147765312&scope=bot"

SERVER_INVITE_LINK = "https://discord.gg/SEnqh73qYj"


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Check bot latency."""
        embed = discord.Embed(colour=discord.Colour.dark_blue())
        embed.add_field(
            name="Pong!",
            value=(f"Latency: {round(self.bot.latency * 1000)}ms"),
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Invites bot to your server."""
        await ctx.send(BOT_INVITE_LINK)

    @commands.command()
    async def server(self, ctx):
        """Sends link of support server"""
        await ctx.send(SERVER_INVITE_LINK)

    @commands.command(aliases=["dev"])
    async def developer(self, ctx):
        """Tells about developer"""
        await ctx.send(embed=dev_embed())

    @commands.command(aliases=["status"])
    async def stats(self, ctx):
        """Bot status."""
        await ctx.send(embed=stats_embed(self.bot))


def setup(bot):
    x = General(bot)
    bot.add_cog(x)
