from discord.ext import commands
from aiohttp import ClientSession
from quora import User
from bot.database import userprofile_api as api
from bot.utils import (
    extract_quora_username,
    profile_embed,
)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._session = None

    async def _create_session(self):
        self._session = ClientSession()

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
    async def profile(self, ctx, quora_username=None):
        """Gives details of any Quora profile."""
        if self._session is None:
            await self._create_session()
        if len(ctx.message.mentions) > 0:
            discord_id = ctx.message.mentions[0].id
            if not api.does_user_exist(discord_id):
                await ctx.reply("Mentioned user's username not found on database.")
                return
            quora_username = api.get_quora_username(discord_id)
        elif quora_username is None:
            if not api.does_user_exist(ctx.author.id):
                await ctx.send(
                    "Either setup your profile first or pass a username with the command."
                )
                return
            quora_username = api.get_quora_username(ctx.author.id)
        user = User(quora_username, session=self._session)
        try:
            profile = await user.profile()
        except ProfileNotFoundError:
            await ctx.reply(
                f"No Quora profile found with the username {quora_username}."
            )
            return
        await ctx.send(embed=profile_embed(profile))


def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
