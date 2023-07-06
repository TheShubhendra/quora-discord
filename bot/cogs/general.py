import asyncio
import pip
import subprocess
import sys

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
        self.embed = self.bot.default_embed

    @commands.command()
    async def ping(self, ctx):
        """Check bot latency."""
        embed = discord.Embed(title="Pong!", colour=discord.Colour.green())
        embed.add_field(
            name="Latency",
            value=f"{round(self.bot.latency * 1000)}ms",
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
        embed = self.embed
        embed.add_field(
            name="Shubhendra Kushwaha",
            value="**GitHub:** https://github.com/TheShubhendra\n**Quora:** https://www.quora.com/profile/Shubhendra-Kushwaha-1",
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["status"])
    async def stats(self, ctx):
        """Bot status."""
        embed = self.embed
        all_tasks = asyncio.tasks.all_tasks()
        files, lines = count("./bot")
        bot = self.bot
        embed.add_field(
            name="Basic Stats",
            value=f"**Server Connected:** {len(bot.guilds)}\n**User Connected:** {len(bot.users)}\n**Total Commands:** {len(bot.commands)}\n**Linked profiles:** {bot.db.profile_count()}",
        )

        embed.add_field(
            name="Program info",
            value=f"**Active Tasks:** {len(all_tasks)}\n**Uptime:** {bot.up_time} second\n**Latency:** {bot.latency * 10000} ms",
        )

        embed.add_field(
            name="Code Info",
            value=f"**Total files:** {files}\n**Code length:** {lines} lines",
        )

        version = sys.version_info
        embed.add_field(
            name="Versions",
            value=f"**Python:** {version.major}.{version.minor}.{version.micro}\n**discord.py:** {discord.__version__}\n**pip:** {pip.__version__}",
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["language", "lang"])
    async def langs(self, ctx):
        """Get the languages and codes."""
        string = ""
        for i, j in subdomains.items():
            string += f"{i} : {j}\n"
        await ctx.send(
            embed=discord.Embed(
                title="Quora languages",
                description=string,
            )
        )

    @commands.command(aliases=["lib"])
    async def libraries(self, ctx):
        """Installed Python libraries ."""
        libs = subprocess.check_output(["pip", "freeze"]).decode("ascii")
        embed = discord.Embed(
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
