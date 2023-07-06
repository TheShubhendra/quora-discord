import logging

from discord.ext import commands
from aiohttp import ClientSession


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.db = self.bot.db

    @commands.command(
        name="list",
        usage="q!list",
        help="Use this command to list all Quorans registerd with the bot in this guild.",
        brief="List all the quorans of the Server.",
    )
    async def quoran_list(self, ctx):
        guild = ctx.guild
        q_list = await self.generate_quorans_list(guild)
        await ctx.reply(f"```\n{self.bot.embed.quoran_list(q_list)}\n```")

    async def generate_quorans_list(self, guild):
        cache_key = "guild_quoran_list_" + str(guild.id)
        q_list = self.bot._cache.get(cache_key)
        if q_list is not None:
            return q_list
        else:
            q_list = []
        async with ClientSession() as session:
            async for member in guild.fetch_members():
                if member.bot:
                    continue
                if self.db.does_user_exist(member.id):
                    try:
                        username = self.db.get_quora_username(member.id)
                        profile = await self.bot.get_quora(
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
        self.bot._cache.set(cache_key, q_list, time=3600)
        return q_list


async def setup(bot):
    cog = Server(bot)
    await bot.add_cog(cog)
