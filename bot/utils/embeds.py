import asyncio
import logging
import pip
import sys
from typing import (
    Any,
    Dict,
    List,
)

import discord
from discord import (
    Colour,
    Embed,
)
from discord.ext.commands import (
    Cog,
    Command,
    )
from quora import (
    Profile,
    Answer,
    Topic,
)

from .misc import count_file_and_lines as count
from .parser import create_profile_link


class EmbedBuilder:
    """Class to build embeds for Quora Bot."""

    def __init__(self, bot: "QuoraBot") -> None:
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_default(self, *args: Any, **kwargs: Any) -> Embed:
        embed = Embed(*args, **kwargs)
        embed.set_footer(
            text="Send q!help to know about the commands or type q!help <command> for help for specific command."
        )
        return embed

    def profile(self, profile: Profile) -> None:
        embed = self.get_default(
            title=profile.username,
            colour=Colour.random(),
        )
        embed.set_thumbnail(url=str(profile.profileImage))
        try:
            embed.add_field(
                name="General⚙️",
                value="**First Name:** {0.firstName}\n"+
                 "**Last Name:** {0.lastName}\n**Crendential:** {0.profileCrendential}\n"+
                 "**Contributing Space:** {0.contributingSpaceCount}".format(profile),
            )
        except Exception as e:
            self.logger.exception(e)

        try:
            embed.add_field(
                name="Views👀",
                value="**Answer Views:** {0.answerViewsCount}\n**Content Views:** {0.contentViewsCount}\n**Last Month Content View:** {0.lastMonthContentView}".format(
                    profile
                ),
            )
        except Exception as e:
            self.logger.exception(e)

        try:
            embed.add_field(
                name="Counts🔢",
                value="**Answer Count:** {0.answerCount}\n**Question Count:** {0.questionCount}\n**Post Count:** {0.postCount}\n**Share Count:** {0.shareCount}".format(
                    profile
                ),
            )
        except Exception as e:
            self.logger.exception(e)

        try:
            embed.add_field(
                name="Follow Counts📜",
                value="**Follower:** {0.followerCount}\n**Following Count:** {0.followingCount}\n**Following Space:** {0.followingSpaceCount}\n**Following Topics:** {0.followingTopicCount}".format(
                    profile
                ),
            )
        except Exception as e:
            self.logger.exception(e)
        try:
            embed.set_author(
                name=profile.firstName + " " + profile.lastName,
                url=create_profile_link(profile.username),
                icon_url=profile.profileImage,
            )
        except Exception as e:
            self.logger.exception(e)
        return embed

    def profile_bio(self, profile: Profile):
        embed = self.get_default(
            title=profile.username,
            colour=Colour.random(),
        )
        try:
            embed.set_image(url=profile.profileImage)
        except Exception as e:
            self.logger.exception(e)
        try:
            embed.set_author(
                name=profile.firstName + " " + profile.lastName,
                url=create_profile_link(profile.username),
                icon_url=profile.profileImage,
            )
        except Exception as e:
            self.logger.exception(e)
        if len(profile.profileBio) <= 1024:
            embed.add_field(name="Profile Bio", value=profile.profileBio)
        else:
            return None
        return embed


    def answers(self, profile: Profile, answers: List[Answer]) -> Embed:
        embed = Embed(
            title=profile.username,
            colour=Colour.random(),
        )
    
        for answer in answers:
            embed.add_field(
                name=str(answer.question),
                value=(
                    str(answer) + f"[Read here]({answer.url})"
                    if len(str(answer)) < 200
                    else str(answer)[:200] + f".....[Read more]({answer.url})"
                ),
            )
        try:
            embed.set_thumbnail(url=str(profile.profileImage))
        except Exception as e:
            self.logger.exception(e)
        try:
            embed.set_author(
                name=profile.firstName + " " + profile.lastName,
                url=create_profile_link(profile.username),
                icon_url=profile.profileImage,
            )
        except Exception as e:
            self.logger.exception(e)
        return embed

    def dev(self) -> Embed:
        embed = self.get_default(
            title="My Developer",
            colour=Colour.random(),
        )
        embed.add_field(
            name="Shubhendra Kushwaha",
            value="**GitHub:** https://github.com/TheShubhendra\n**Quora:** https://www.quora.com/profile/Shubhendra-Kushwaha-1",
        )
        return embed

    def help_embed(self, title: str = "Quora Bot Help"):
        embed = self.get_default(
            title=title,
            colour=Colour.from_rgb(255, 0, 0),
        )
        embed.set_author(
            name="Quora",
            icon_url="https://cdn.discordapp.com/avatars/838250557805821992/cd60e572bded2f16ea97dff916da481c.png?size=256",
        )
        return embed

    def bot_help(
        self,
        mapping: Dict[Cog, List[Command]],
        prefix: str = "q!",
    ) -> Embed:
        embed = self.help_embed()
        self.logger.info(embed.to_dict())
        for cog, commands in mapping.items():
            if commands is None or len(commands) < 1:
                continue
            if getattr(cog, "qualified_name", "") == "Admin":
                continue
            cmd_str = ""
            for command in commands:
                cmd_str += f"{prefix}{command.qualified_name} - {command.short_doc}\n"
            embed.add_field(
                name=getattr(cog, "qualified_name", "Other"),
                value=cmd_str,
                )
        embed.add_field(
            name=getattr(cog, "qualified_name", "Other"),
            value=cmd_str,
        )
        return embed

    def command_help(
        self,
        command: Command,
        prefix: str = "q!",
    ):
        embed = self.help_embed(title=f"{command.qualified_name} command help")
        embed.add_field(
            name="Help",
            value=command.help if command.help else command.short_doc,
        )
        if command.usage is not None:
            embed.add_field(
                name="Example",
                value=command.usage,
            )
        return embed

    def knows_about(
        self,
        profile: Profile,
        knows_about: List[Topic],
    ) -> Embed:
        embed = self.get_default(
            title=profile.username,
            colour=Colour.random(),
        )
        for topic in knows_about:
            embed.add_field(
                name=topic.name,
                value=f"[{str(topic.userAnswersCount)} answers by {profile.firstName}]({topic.userAnswersUrl}) on **[{topic.name}]({topic.url})** (Followed by {topic.followerCount})",
            )
        try:
            embed.set_thumbnail(url=str(profile.profileImage))
        except Exception as e:
            self.logger(e)
        try:
            embed.set_author(
                name=profile.firstName + " " + profile.lastName,
                url=create_profile_link(profile.username),
                icon_url=profile.profileImage,
            )
        except Exception as e:
            self.logger.exception(e)
        return embed

    def profile_pic(self, profile: Profile) -> Embed:
        embed = self.get_default(
            title=profile.username,
            colour=Colour.random(),
        )
        embed.set_image(url=profile.profileImage)
        return embed

    def stats(self) -> Embed:
        all_tasks = asyncio.tasks.all_tasks()
        files, lines = count("./bot")
        embed = self.get_default(
            name="Quora Bot Status",
            colour=Colour.random(),
        )
        bot = self.bot
        embed.add_field(
            name="Basic Stats",
            value=f"**Server Connected:** {len(bot.guilds)}\n**User Connected:** {len(bot.users)}\n**Total Commands:** {len(bot.commands)}\n**Linked profiles:** {bot.db.profile_count()}",
        )

        embed.add_field(
            name="Program info",
            value=f"**Active Tasks:** {len(all_tasks)}\n**Uptime:** {bot.up_time} second\n**Latency:** {bot.latency*10000} ms",
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
        return embed
