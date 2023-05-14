import discord
from discord.ext import commands
from typing import Optional
from ..utils.embeds._profileEmbed import profile_view
from ..utils.embeds._generalEmbed import profileNotFound
from ..utils.ui.profileUi import ProfileDropdownView
from ..utils.parser.usernameParser import getQuoraUsername
from quora import User


class UserProfile(commands.Cog):
    """class to generate general commands for bot

    Args:
        None
    Inherits:
        Inherits discord.ext.commands.Cog
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @discord.app_commands.command(name="profile", description="Fetches the profile")
    @discord.app_commands.describe(
        member="mention the user", username="Give your Quora Username or Link"
    )
    async def profile(
        self,
        interaction: discord.Interaction,
        member: Optional[discord.Member],
        username: Optional[str],
    ):
        member = member if member is not None else interaction.user
        if username is None:
            username = self.bot.db.getQuoraUsername(member.id)
        try:
            quoraUser = User(username=username, cache_manager=self.bot.cacheManager)
            userDataProfile = await quoraUser.profile()
            userDataAnswers = await quoraUser.answers()
            userDataKnows = await quoraUser.knows_about()
            view = ProfileDropdownView(
                interaction,
                self.bot,
                userDataProfile,
                userDataAnswers,
                userDataKnows,
            )
            embed = profile_view(member, userDataProfile, self.bot)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await interaction.response.send_message(
                embed=profileNotFound(self.bot, interaction.user), ephemeral=True
            )
            print(e)


async def setup(bot) -> None:
    await bot.add_cog(UserProfile(bot))

    # if _username is None:
    #     self.bot.db.addQuoraUsername(discord_id=member.id,
    #                                  quora_username=username,
    #                                  discord_username=member.name,
    #                                  follower_count=userDataProfile.followerCount)
