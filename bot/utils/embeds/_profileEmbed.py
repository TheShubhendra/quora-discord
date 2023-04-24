import discord
from quora import User
from datetime import datetime
import quora


async def profile_view(interaction_user: discord.Member, user_data: quora.Profile) -> discord.Embed:
    fullname = (user_data.firstName + ' ' + user_data.lastName).strip()
    embed = discord.Embed(title=f'{user_data.username}',
                          url=f'https://www.quora.com/profile/{user_data.username}',
                          color=discord.Colour.red())
    embed.set_author(name=fullname,
                     icon_url=user_data.profileImage)
    embed.set_thumbnail(url=user_data.profileImage)
    embed.add_field(name='General',
                    value=f"Name: {fullname}\nCrendential: {user_data.profileCrendential}\nContributing Spaces: {user_data.contributingSpaceCount}",
                    inline=True)
    embed.add_field(name='Views',
                    value=f"Answer Views: {user_data.answerViewsCount}\nContent Views: {user_data.contentViewsCount}\nLast Month Content Views: {user_data.lastMonthContentView}",
                    inline=True)
    embed.add_field(name='Counts',
                    value=f"Answer Count: {user_data.answerCount}\nQuestions Count: {user_data.questionCount}\nPost Count: {user_data.postCount}\nShare Count: {user_data.shareCount}",
                    inline=True)
    embed.add_field(name='Follow Counts',
                    value=f"Followers Count: {user_data.followerCount}\nFollowing Count: {user_data.followingCount}\nFollowing Spaces: {user_data.followingSpaceCount}\nFollowing Topics: {user_data.followingTopicCount}",
                    inline=True)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url,
    )
    return embed
