import logging
from discord.ext import commands
from aiohttp import ClientSession
from quora import User
from quora.exceptions import ProfileNotFoundError
from bot.database import userprofile_api as api
from discord_components import DiscordComponents, Button, Select, SelectOption
from bot.utils import (
    extract_quora_username,
    profile_embed,
    profile_pic_embed,
    profile_bio_embed,
    answers_embed,
    knows_about_embed,
)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._session = None
        self.logger = logging.getLogger(__name__)
        self.components = [
            Select(
                placeholder="Select sections",
                options=[
                    SelectOption(
                        label="General Profile",
                        value="profile",
                    ),
                    SelectOption(
                        label="Profile Picture",
                        value="pic",
                    ),
                    SelectOption(
                        label="Profile Bio",
                        value="bio",
                    ),
                    SelectOption(
                        label="Latest Answers",
                        value="answers",
                    ),
                    SelectOption(
                        label="Knows about",
                        value="knows",
                    ),
                ],
            )
        ]

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
        quora_username_or_profile_link,
        user_id=None,
    ):
        """Links your Quora profile."""
        if user_id is None:
            user_id = ctx.author.id
        username = extract_quora_username(quora_username_or_profile_link)
        if username is None:
            await ctx.reply("Username or profile link is not valid")
            return
        try:
            profile = await User(username).profile()
        except ProfileNotFoundError:
            await ctx.reply("Username or profile link is not valid")
            return
        if api.does_user_exist(str(user_id), check_hidden=True):
            api.update_quoran(
                str(user_id), username, profile.followerCount, profile.AnswerCount
            )
        else:
            api.add_user(
                user_id,
                ctx.author.name,
                username,
                profile.followerCount,
                profile.answerCount,
            )
        await ctx.reply(
            f"Your username {username} has been successfully updated in the database."
        )

    @commands.command(
        help="Use this command to remove your linked Quora profile with this bot.",
        brief="Unlink your Quora profile.",
    )
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

    @commands.command(
        aliases=["p"],
        help="Use this command to fetch a Quora profile.\n**Usage**\n1. q!profile\n2. q!profile <mention someone>.\n3. q!profile <Username of the quoran.",
        usage="q!profile\nq!profile Shubhendra-Kushwaha-1\nq!profile <@72863363373337>",
        brief="Fetch a Quora profile.",
    )
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
            self.logger.exception("No profile found")
            await ctx.reply(
                f"No Quora profile found with the username `{quora_username}`."
            )
            await self.bot.log(
                f"No Quora profile found with the username {quora_username}.\nChannel: {ctx.channel.mention}"
            )

        await ctx.send(
            embed=profile_embed(profile),
            components=self.components,
        )
        while True:
            try:
                interaction = await self.bot.wait_for("select_option")
            except Exception as e:
                self.logger.exception(str(e))
            selection = interaction.component[0].value
            self.logger.info(selection)
            if selection == "profile":
                embed = profile_embed(profile)
            elif selection == "pic":
                embed = profile_pic_embed(profile)
            elif selection == "bio":
                embed == profile_bio_embed(profile)
            elif selection == "answers":
                answers = await user.answers()
                embed = answers_embed(profile, answers)
            elif selection == "knows":
                knows_about = await user.knows_about()
                embed = knows_about_embed(profile, knows_about)
            else:
                continue
            try:
                await interaction.message.edit(
                    embed=embed,
                    components=self.components,
                )
            except:
                self.logger.exception("Error")

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
        try:
            user = User(quora_username, session=self._session)
            profile = await user.profile()
        except ProfileNotFoundError:
            await ctx.reply(
                f"No Quora profile found with the username `{quora_username}`."
            )
            return
        await ctx.send(embed=profile_pic_embed(profile))

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
        user = User(quora_username, session=self._session)
        profile = await user.profile()
        answers = await user.answers()

        embed = answers_embed(profile, answers)
        await ctx.reply(embed=embed)

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
        if quora_username is None:
            return
        user = User(quora_username, session=self._session)
        profile = await user.profile()
        knows_about = await user.knows_about()

        embed = knows_about_embed(profile, knows_about)
        await ctx.reply(embed=embed)


def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
