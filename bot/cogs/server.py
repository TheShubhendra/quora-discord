import logging

from discord.ext import commands
from aiohttp import ClientSession

from .profile import User


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.db = self.bot.db

    @commands.command(name="list")
    async def quoran_list(self, ctx):
        guild = ctx.guild
        q_list = []
        async with ClientSession() as session:
            async for member in guild.fetch_members():
                if member.bot:
                    continue
                if self.db.does_user_exist(member.id):
                    try:
                        username = self.db.get_quora_username(member.id)
                        profile = await User(
                            username,
                            session=session,
                            cache_manager=self.bot._cache,
                        ).profile()
                        q_list.append(
                            (
                                member.name,
                                username,
                                profile.followerCount,
                                profile.contentViewsCount,
                            )
                        )
                    except:
                        self.logger.exception(f"Error in {username}")
        await ctx.reply(f"```\n{self.bot.embed.quoran_list(q_list)}\n```")


def setup(bot):
    cog = Server(bot)
    bot.add_cog(cog)
