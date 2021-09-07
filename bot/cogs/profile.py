import logging
from asyncio import TimeoutError
from discord.ext import commands
from discord.ext.commands import CommandError
from aiohttp import ClientSession
from quora import User as QuoraUser
from quora.exceptions import ProfileNotFoundError
from discord_components import DiscordComponents, Button, Select, SelectOption
from bot.utils import (
    extract_quora_username,
)
from bot.mixins import ProfileHelper


class User(QuoraUser):
    def profile(self, cache_exp=180):
        return super().profile(self, cache_exp=cache_exp)

    def knows_about(self, cache_exp=3600):
        return super().knows_about(self, cache_exp=cache_exp)

    def answers(self, cache_exp=300):
        return super().answers(self, cache_exp=cache_exp)


class Profile(ProfileHelper, commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.embed = self.bot.embed
        self._session = None
        self.logger = logging.getLogger(__name__)

    async def _create_session(self):
        self.logger.debug("Creating a session.")
        self._session = ClientSession()

    @commands.command(
        usage="q!setprofile Shubhendra-Kushwaha-1\nor q!setprofile https://www.quora.com/profile/Shubhendra-Kushwaha-1",
        help="Use this command to link your quora profile with this bot\nUsage: q!setprofile <Quora username or profile link>",
        brief="Links your Quora profile.",
    )
    async def setprofile(
        self,
        ctx,
        username=None,
    ):
        """Links your Quora profile."""
        await self._setprofile_view(ctx, username)

    @commands.command(
        help="Use this command to remove your linked Quora profile with this bot.",
        brief="Unlink your Quora profile.",
    )
    async def remove(self, ctx):
        """Remove your Quora profile from bot."""
        if self.bot.db.does_user_exist(ctx.author.id):
            self.bot.db.update_access(ctx.author.id, "none")
            await ctx.reply("Profile removed successfully.")
        else:
            await ctx.reply("No linked profile found.")

    @commands.command(
        aliases=["p"],
        name="profile",
        help="Use this command to fetch a Quora profile.\n**Usage**\n1. q!profile\n2. q!profile <mention someone>.\n3. q!profile <Username of the quoran.",
        usage="q!profile\nq!profile Shubhendra-Kushwaha-1\nq!profile <@72863363373337>",
        brief="Fetch a Quora profile.",
    )
    async def fetch_profile(self, ctx, quora_username=None):
        """Gives details of any Quora profile."""
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, quora_username)
        if quora_username is None:
            return
        await self._generate_view(ctx, quora_username, "profile", "en")

    @commands.command(
        aliases=["picture", "pfp", "dp"],
        help="Use this command to fetch a Quora profile.\n**Usage**\n1. q!pic\n2. q!profile <mention someone>.\n3. q!pic <Username of the quoran.",
        usage="q!pic\nq!pic Shubhendra-Kushwaha-1\nq!pic <@72863363373337>",
        brief="Fetch profile picture of a Quora profile.",
    )
    async def pic(self, ctx, args=None):
        """Show the profile picture of Quora profile."""
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, args)
        if quora_username is None:
            return
        await self._generate_view(ctx, quora_username, "pic", "en")

    @commands.command(
        aliases=["profileBio", "intro"],
        help="Use this command to fetch a Quora profile.\n**Usage**\n1. q!bio\n2. q!bio <mention someone>.\n3. q!bio <Username of the quoran.",
        usage="q!bio\nq!bio Shubhendra-Kushwaha-1\nq!bio <@72863363373337>",
        brief="Fetch the profile bio of a Quora profile",
    )
    async def bio(self, ctx, args=None):
        """Show the profile bio of Quora user."""
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, args)
        if quora_username is None:
            return
        await self._generate_view(ctx, quora_username, "bio", "en")

    @commands.command(
        aliases=["a"],
        help="Use this command to fetch a Quora profile.\n**Usage**\n1. q!answers\n2. q!answers <mention someone>.\n3. q!answers<Username of the quoran.",
        usage="q!answers\nq!answers Shubhendra-Kushwaha-1\nq!profile <@72863363373337>",
        brief="Fetch pinned and recent answers",
    )
    async def answers(self, ctx, args=None):
        """Shows pinned and recent answers."""
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, args)
        if quora_username is None:
            return
        await self._generate_view(ctx, quora_username, "answers", "en")

    @commands.command(
        aliases=["knows_about", "k"],
        help="Get top few topics on which user has written most of the answers.",
        usage="q!knows \nq!knows Shubhendra-Kushwaha-1\nq!knows <@72863363373337>",
        brief="Fetch knows about section.",
    )
    async def knows(self, ctx, args=None):
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, args)
        await self._generate_view(ctx, quora_username, "pic", "en")


def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
