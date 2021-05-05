from discord import Embed, Colour


def profile_embed(profile):
    embed = Embed(
        title=profile.username,
        colour=Colour.random(),
    )
    # for i,j in vars(profile).items():
    # embed.add_field(name=i, value=j)
    embed.set_thumbnail(url=str(profile.profileImage))
    embed.add_field(
        name="General",
        value="**First Name:** {0.firstName}\n**Last Name:** {0.lastName}\n**Crendential:** {0.profileCrendential}\n**Contributing Space:** {0.contributingSpaceCount}".format(
            profile
        ),
    )

    embed.add_field(
        name="Views",
        value="**Answer Views:** {0.answerViewsCount}\n**Content Views:** {0.contentViewsCount}\n**Last Month Content View:** {0.lastMonthContentView}".format(
            profile
        ),
    )

    embed.add_field(
        name="Counts",
        value="**Answer Count:** {0.answerCount}\n**Question Count:** {0.questionCount}\n**Post Count:** {0.postCount}\n**Share Count:** {0.shareCount}".format(
            profile
        ),
    )

    embed.add_field(
        name="Follow Counts",
        value="**Follower:** {0.followerCount}\n**Following Count:** {0.followingCount}\n**Following Space:** {0.followingSpaceCount}\n**Following Topics:** {0.followingTopicCount}".format(
            profile
        ),
    )

    return embed
