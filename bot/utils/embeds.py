from discord import Embed, Colour
from bot.utils import create_profile_link


class Embed(Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_footer(
            text="Send q!help to know about all commands or type q!help <command> for help for specific command."
        )


def profile_embed(profile):
    embed = Embed(
        title=profile.username,
        colour=Colour.random(),
    )
    embed.set_thumbnail(url=str(profile.profileImage))
    try:
        embed.add_field(
            name="General⚙️",
            value="**First Name:** {0.firstName}\n**Last Name:** {0.lastName}\n**Crendential:** {0.profileCrendential}\n**Contributing Space:** {0.contributingSpaceCount}".format(
                profile
            ),
        )
    except:
        pass

    try:
        embed.add_field(
            name="Views👀",
            value="**Answer Views:** {0.answerViewsCount}\n**Content Views:** {0.contentViewsCount}\n**Last Month Content View:** {0.lastMonthContentView}".format(
                profile
            ),
        )
    except:
        pass
    try:

        embed.add_field(
            name="Counts🔢",
            value="**Answer Count:** {0.answerCount}\n**Question Count:** {0.questionCount}\n**Post Count:** {0.postCount}\n**Share Count:** {0.shareCount}".format(
                profile
            ),
        )
    except:
        pass
    try:
        embed.add_field(
            name="Follow Counts📜",
            value="**Follower:** {0.followerCount}\n**Following Count:** {0.followingCount}\n**Following Space:** {0.followingSpaceCount}\n**Following Topics:** {0.followingTopicCount}".format(
                profile
            ),
        )
    except:
        pass
    try:
        embed.set_author(
            name=profile.firstName + " " + profile.lastName,
            url=create_profile_link(profile.username),
            icon_url=profile.profileImage,
        )
    except:
        pass
    return embed


def profile_pic_embed(profile):
    embed = Embed(
        title=profile.username,
        colour=Colour.random(),
    )
    embed.set_image(url=profile.profileImage)
    return embed


def profile_bio_embed(profile):
    embed = Embed(
        title=profile.username,
        colour=Colour.random(),
    )
    try:
        embed.set_image(url=profile.profileImage)
    except:
        pass
    try:
        embed.set_author(
            name=profile.firstName + " " + profile.lastName,
            url=create_profile_link(profile.username),
            icon_url=profile.profileImage,
        )
    except:
        pass
    if len(profile.profileBio) <= 1024:
        embed.add_field(name="Profile Bio", value=profile.profileBio)
    else:
        return None
    return embed


def answers_embed(profile, answers):
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
    except:
        pas
    try:
        embed.set_author(
            name=profile.firstName + " " + profile.lastName,
            url=create_profile_link(profile.username),
            icon_url=profile.profileImage,
        )
    except:
        pass
    return embed


def dev_embed():
    embed = Embed(
        title="My Developer",
        colour=Colour.random(),
    )
    embed.add_field(
        name="Shubhendra Kushwaha",
        value="**GitHub:** https://github.com/TheShubhendra\n**Quora:** https://www.quora.com/profile/Shubhendra-Kushwaha-1",
    )
    return embed


def help_embed(title="Quora Bot Help"):
    embed = Embed(title=title, colour=Colour.from_rgb(255, 0, 0))
    embed.set_author(
        name="Quora",
        icon_url="https://cdn.discordapp.com/avatars/838250557805821992/cd60e572bded2f16ea97dff916da481c.png?size=256",
    )
    return embed


def bot_help_embed(mapping, prefix="q!"):
    embed = help_embed()
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
    return embed


def command_help_embed(command, prefix="q!"):
    embed = help_embed(title=f"{command.qualified_name} command help")
    embed.add_field(
        name=f"Help",
        value=command.help if command.help else command.short_doc,
    )
    if command.usage is not None:
        embed.add_field(
            name="Example",
            value=command.usage,
        )
    return embed
