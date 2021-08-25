import logging
from asyncio import TimeoutError
from discord.ext import commands
from aiohttp import ClientSession
from quora import User as QuoraUser
from quora.exceptions import ProfileNotFoundError
from discord_components import DiscordComponents, Button, Select, SelectOption
from bot.utils import (
    extract_quora_username,
)


class User(QuoraUser):
    def profile(self, cache_exp=180):
        return super().profile(self, cache_exp=cache_exp)

    def knows_about(self, cache_exp=3600):
        return super().knows_about(self, cache_exp=cache_exp)

    def answers(self, cache_exp=300):
        return super().answers(self, cache_exp=cache_exp)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = self.bot.embed
        self._session = None
        self.select_options = [
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
        ]
        self.logger = logging.getLogger(__name__)
        self.components = [
            Select(
                placeholder="Select sections",
                options=self.select_options,
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
        user=None,
    ):
        """Links your Quora profile."""
        if user is None:
            user = ctx.author
        user_id = user.id
        username = extract_quora_username(quora_username_or_profile_link)
        if username is None:
            await ctx.reply("Username or profile link is not valid")
            return
        try:
            profile = await User(username, cache_manager=self.bot._cache).profile()
        except ProfileNotFoundError:
            self.bot.log(
                f"Error in set profile {username}.\nChannel:\n``` {ctx.channel.mention}\n{ctx.channel}{ctx.channel.id}\n{ctx.channel.guild}\n{ctx.author}"
            )
            await ctx.reply("Username or profile link is not valid")
            return
        if self.bot.db.does_user_exist(str(user_id), check_hidden=True):
            self.bot.db.update_quoran(
                str(user_id), username, profile.followerCount, profile.answerCount
            )
        else:
            self.bot.db.add_user(
                user_id,
                user.name + "#" + str(user.discriminator),
                username,
                profile.followerCount,
                profile.answerCount,
            )
        await ctx.reply(
            f"{user.mention}'s ' username {username} has been successfully updated in the database."
        )

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

    async def get_username(self, ctx, quora_username=None):
        if len(ctx.message.mentions) > 0:
            discord_id = ctx.message.mentions[0].id
            if not self.bot.db.does_user_exist(discord_id):
                await ctx.reply("Mentioned user's username not found on database.")
                return
            quora_username = self.bot.db.get_quora_username(discord_id)
        elif quora_username is None:
            if not self.bot.db.does_user_exist(ctx.author.id):
                await ctx.send(
                    "Either setup your profile first or pass a username with the command."
                )
                return
            quora_username = self.bot.db.get_quora_username(ctx.author.id)
        return quora_username

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
        user = User(
            quora_username, session=self._session, cache_manager=self.bot._cache
        )
        try:
            profile = await user.profile()
        except ProfileNotFoundError:
            self.logger.exception("No profile found")
            await ctx.reply(
                f"No Quora profile found with the username `{quora_username}`."
            )
            await self.bot.log(
                f"No Quora profile found with the username {quora_username}.\nChannel:\n``` {ctx.channel.mention}\n{ctx.channel}{ctx.channel.id}\n{ctx.channel.guild}\n{ctx.author}"
            )
            return
        message = await ctx.send(
            embed=self.embed.profile(profile),
            components=self.components,
        )
        while True:
            try:
                interaction = await self.bot.wait_for(
                    "select_option",
                    check=lambda i: i.message == message,
                    timeout=30,
                )
            except TimeoutError:
                await message.edit(
                    components=[
                        Select(
                            placeholder="Select sections",
                            options=self.select_options,
                            disabled=True,
                        )
                    ]
                )
                return
            except Exception as e:
                self.logger.exception(str(e))
                continue
            if interaction.user != ctx.author and interaction.user.id != self.bot.owner_id:
                await interaction.respond(
                    content="You are not allowed to interact with this message.",
                )
                continue
            selection = interaction.values[0]
            if selection == "profile":
                embed = self.embed.profile(profile)
            elif selection == "pic":
                embed = self.embed.profile_pic(profile)
            elif selection == "bio":
                embed == self.embed.profile_bio(profile)
            elif selection == "answers":
                answers = await user.answers()
                embed = self.embed.answers(profile, answers)
            elif selection == "knows":
                knows_about = await user.knows_about()
                embed = self.embed.knows_about(profile, knows_about)
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
            user = User(
                quora_username, session=self._session, cache_manager=self.bot._cache
            )
            profile = await user.profile()
        except ProfileNotFoundError:
            await ctx.reply(
                f"No Quora profile found with the username `{quora_username}`."
            )
            return
        await ctx.send(embed=self.embed.profile_pic(profile))

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
            user = User(
                quora_username, session=self._session, cache_manager=self.bot._cache
            )
            profile = await user.profile()
        except ProfileNotFoundError:
            await ctx.reply(
                f"No Quora profile found with the username `{quora_username}`."
            )
            return
        embed = self.embed.profile_bio(profile)
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
        user = User(
            quora_username, session=self._session, cache_manager=self.bot._cache
        )
        profile = await user.profile()
        answers = await user.answers()

        embed = self.embed.answers(profile, answers)
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
        user = User(
            quora_username, session=self._session, cache_manager=self.bot._cache
        )
        profile = await user.profile()
        knows_about = await user.knows_about()

        embed = self.embed.knows_about(profile, knows_about)
        await ctx.reply(embed=embed)


def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
