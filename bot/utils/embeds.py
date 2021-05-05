from discord import Embed, Colour


def profile_embed(profile):
    embed = Embed(
        title=profile.username,
        colour = Colour.random(),
    )
    #for i,j in vars(profile).items():
        #embed.add_field(name=i, value=j)
    embed.set_thumbnail(url=str(profile.profileImage))
    embed.add_field(name = "First Name", value = profile.firstName, inline=True)
    embed.add_field(name = "Last Name", value = profile.lastName, inline=True)
    embed.add_field(name = "Credential", value = profile.profileCrendential)
    embed.add_field(name = "Contributing Space", value = profile.contributingSpaceCount)
    embed.add_field(name = "Answer Views", value = profile.answerViewsCount)
    embed.add_field(name = "Content Views", value = profile.contentViewsCount)
    embed.add_field(name = "Last month content views", value = profile.lastMonthContentView)
    embed.add_field(name = "Answer Count", value = profile.answerCount)
    embed.add_field(name = "Question Count", value = profile.questionCount)
    embed.add_field(name = "Post Count", value = profile.postCount)
    embed.add_field(name = "Share Count", value = profile.shareCount)
    embed.add_field(name = "Followers", value = profile.followerCount)
    embed.add_field(name = "Following", value = profile.followingCount)
    embed.add_field(name = "Following Space", value = profile.followingSpaceCount)
    embed.add_field(name = "Following Topics", value = profile.followingTopicCount)
    return embed
