from discord.ext import commands
from aiohttp import ClientSession
from quora import User
from quora.exceptions import ProfileNotFoundError
from bot.database import userprofile_api as api
from bot.utils import (
    extract_quora_username,
    profile_embed,
    profile_pic_embed,
    profile_bio_embed,
    answers_embed,
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
            _ = await User(username).profile()
        except:
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
    async def remove(self, ctx):
        """Remove your Quora profile from bot."""
        if api.does_user_exist(ctx.author.id):
            api.update_access(ctx.author.id, "none")
            await ctx.reply("Profile removed successfully.")
        else:
            await ctx.reply("No linked profile found.")

    async def get_username(self, ctx, quora_username=None):
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
        return quora_username

    @commands.command(aliases=["p"])
    async def profile(self, ctx, quora_username=None):
        """Gives details of any Quora profile."""
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, quora_username)
        if quora_username is None:
            return
        user = User(quora_username, session=self._session)
        try:
            profile = await user.profile()
        except ProfileNotFoundError:
            await ctx.reply(
                f"No Quora profile found with the username `{quora_username}`."
            )
            return
        except Exception as e:
            await ctx.reply("```\n" + str(e) + "\n```")
            return
        try:
            await ctx.send(embed=profile_embed(profile))
        except Exception as e:
            await ctx.reply(e)

    @commands.command(aliases=["picture", "pfp", "dp"])
    async def pic(self, ctx, args=None):
        """Show the profile picture of Quora profile."""
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, args)
        if quora_username is None:
            return
        try:
            user = User(quora_username, session=self._session)
            profile = await user.profile()
        except ProfileNotFoundError:
            await ctx.reply(
                f"No Quora profile found with the username `{quora_username}`."
            )
            return
        await ctx.send(embed=profile_pic_embed(profile))

    @commands.command(aliases=["profileBio", "intro"])
    async def bio(self, ctx, args=None):
        """Show the profile bio of Quora user."""
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, args)
        if quora_username is None:
            return
        try:
            user = User(quora_username, session=self._session)
            profile = await user.profile()
        except ProfileNotFoundError:
            await ctx.reply(
                f"No Quora profile found with the username `{quora_username}`."
            )
            return
        embed = profile_bio_embed(profile)
        if embed is not None:
            await ctx.send(embed=embed)
        elif len(profile.profileBio) <= 1992:
            await ctx.send("```\n" + profile.profileBio + "\n```")
        else:
            bio = profile.profileBio
            while True:
                if len(bio) >= 1500:
                    await ctx.send("```\n" + bio[:1500] + "```\n")
                elif len(bio) == 0:
                    break
                else:
                    await ctx.send("```\n" + bio + "\n```")
                bio = bio[1500:]

    @commands.command(aliases=["a"])
    async def answers(self, ctx, args=None):
        """Shows pinned and recent answers."""
        if self._session is None:
            await self._create_session()
        quora_username = await self.get_username(ctx, args)
        if quora_username is None:
            return
        user = User(quora_username, session=self._session)
        try:
            profile = await user.profile()
            answers = await user.answers()

            embed = answers_embed(profile, answers)
            await ctx.reply(embed=embed)
        except Exception as e:
            await ctx.reply("```\n" + str(e) + "\n```")


def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
