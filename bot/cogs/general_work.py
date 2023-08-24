import asyncio
import subprocess
from discord.ext import commands
import discord
from bot.utils import count_file_and_lines as count
import logging
from quora.user import subdomains

BOT_INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=838250557805821992&permissions=2147765312&scope=bot"

SERVER_INVITE_LINK = "https://discord.gg/SEnqh73qYj"


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = self.bot.embed
        self.logger = logging.getLogger(__name__)

    @commands.hybrid_command(name="ping", with_app_command=True)
    async def ping(self, ctx: commands.Context, command: str = None):
        """Check bot latency."""
        embed = self.embed.get_default(colour=discord.Colour.dark_blue())
        embed.add_field(
            name="Pong!",
            value=(f"Latency: {round(self.bot.latency * 1000)}ms"),
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="invite", with_app_command=True)
    async def invite(self, ctx):
        """Invites bot to your server."""
        await ctx.send(BOT_INVITE_LINK)

    @commands.hybrid_command(name="server", with_app_command=True)
    async def server(self, ctx):
        """Sends link of support server"""
        await ctx.send(SERVER_INVITE_LINK)

    @commands.hybrid_command(name="developer", with_app_command=True, aliases=["dev"])
    async def developer(self, ctx):
        """Tells about developer"""
        await ctx.send(embed=self.embed.dev())

    @commands.hybrid_command(name="stats", with_app_command=True, aliases=["status"])
    async def stats(self, ctx):
        """Bot status."""
        await ctx.send(embed=self.embed.stats())

    @commands.hybrid_command(name="langs", with_app_command=True, aliases=["languages", "lang"])
    async def langs(self, ctx):
        """Get the languages and codes."""
        string = ""
        for i, j in subdomains.items():
            string += f"{i} : {j}\n"
        await ctx.send(
            embed=self.embed.get_default(
                title="Quora languages",
                description=string,
            )
        )

    @commands.hybrid_command(name="libraries", with_app_command=True, aliases=["libs"])
    async def libraries(self, ctx):
        """Installed Python libraries ."""
        libs = subprocess.check_output(["pip", "freeze"]).decode("ascii")
        embed = self.embed.get_default(
            title="Python libraries",
            colour=discord.Colour.blue(),
        )
        embed.add_field(
            name="Libraries",
            value=libs,
        )
        await ctx.send(embed=embed)


async def setup(bot):
    x = General(bot)
    await bot.add_cog(x)
