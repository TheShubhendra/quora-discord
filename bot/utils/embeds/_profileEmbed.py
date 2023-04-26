import discord
from quora import User
from datetime import datetime
import quora
from discord.ext import commands


def profile_view(
    interaction_user: discord.Member,
    userDataProfile: quora.Profile,
    client: commands.Bot,
) -> discord.Embed:
    fullname = (userDataProfile.firstName + " " +
                userDataProfile.lastName).strip()
    embed = discord.Embed(
        title=f"{userDataProfile.username}",
        url=f"https://www.quora.com/profile/{userDataProfile.username}",
        color=discord.Colour.red(),
    )
    embed.set_author(name=(userDataProfile.firstName + ' ' + userDataProfile.lastName).strip(),
                     icon_url=userDataProfile.profileImage)
    embed.set_thumbnail(url=userDataProfile.profileImage)
    embed.add_field(
        name="General",
        value=f"Name: {fullname}\nCrendential: {userDataProfile.profileCrendential}\nContributing Spaces: {userDataProfile.contributingSpaceCount}",
        inline=True,
    )
    embed.add_field(
        name="Views",
        value=f"Answer Views: {userDataProfile.answerViewsCount}\nContent Views: {userDataProfile.contentViewsCount}\nLast Month Content Views: {userDataProfile.lastMonthContentView}",
        inline=True,
    )
    embed.add_field(
        name="Counts",
        value=f"Answer Count: {userDataProfile.answerCount}\nQuestions Count: {userDataProfile.questionCount}\nPost Count: {userDataProfile.postCount}\nShare Count: {userDataProfile.shareCount}",
        inline=True,
    )
    embed.add_field(
        name="Follow Counts",
        value=f"Followers Count: {userDataProfile.followerCount}\nFollowing Count: {userDataProfile.followingCount}\nFollowing Spaces: {userDataProfile.followingSpaceCount}\nFollowing Topics: {userDataProfile.followingTopicCount}",
        inline=True,
    )
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url,
    )
    return embed


def profile_pic_view(
    interaction_user: discord.Member,
    userDataProfile: quora.Profile,
    client: commands.Bot,
) -> discord.Embed:
    embed = discord.Embed(
        title=userDataProfile.username,
        url=f"https://www.quora.com/profile/{userDataProfile.username}",
        colour=discord.Colour.red(),
    )
    embed.set_author(name=(userDataProfile.firstName + ' ' + userDataProfile.lastName).strip(),
                     icon_url=userDataProfile.profileImage)
    embed.set_image(url=userDataProfile.profileImage)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url,
    )
    return embed


def profile_bio_view(
    interaction_user: discord.Member,
    userDataProfile: quora.Profile,
    client: commands.Bot,
) -> discord.Embed:
    embed = discord.Embed(title=userDataProfile.username,
                          colour=discord.Colour.red())
    embed.set_author(name=(userDataProfile.firstName + ' ' + userDataProfile.lastName).strip(),
                     icon_url=userDataProfile.profileImage)
    embed.add_field(name="Bio",
                    value=userDataProfile.profileBio)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url,
    )
    return embed


def profile_answers_view(
    interaction_user: discord.Member,
    userDataProfile: quora.Profile,
    userDataAnswers: quora.Answer,
    client: commands.Bot,
) -> discord.Embed:
    embed = discord.Embed(title=userDataProfile.username,
                          colour=discord.Colour.red())
    embed.set_author(name=(userDataProfile.firstName + ' ' + userDataProfile.lastName).strip(),
                     icon_url=userDataProfile.profileImage)
    for index, answer in zip(range(len(userDataAnswers)), userDataAnswers):
        embed.add_field(name=f'{index +1}) ' + str(answer.question),
                        value=str(answer)[:200] + f' [read more]({answer.url})', inline=True)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url,
    )
    return embed


def profile_topic_view(
    interaction_user: discord.Member, userDataProfile: quora.Profile, userDataTopic: quora.Topic, client: commands.Bot
) -> discord.Embed:
    embed = discord.Embed(title=userDataProfile.username,
                          url=userDataProfile.profileImage, colour=discord.Colour.red())
    embed.set_author(name=(userDataProfile.firstName + ' ' + userDataProfile.lastName).strip(),
                     icon_url=userDataProfile.profileImage)
    for topic in userDataTopic:
        embed.add_field(
            name=topic.name,
            value=f"{str(topic.userAnswersCount)} answers by {userDataProfile.firstName} on **[{topic.name}]({topic.url})** (Followed by {topic.followerCount})",
            inline=True
        )
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url,
    )
    return embed


def help_command_embed(
    interaction_user: discord.Member, client: commands.Bot
) -> discord.Embed:
    embed = discord.Embed(colour=discord.Colour.red())
    embed.set_author(name="Quora", icon_url=client.user.avatar.url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url,
    )
    return embed
