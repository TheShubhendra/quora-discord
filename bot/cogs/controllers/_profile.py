import discord
from discord.ext import commands
from typing import Optional
from ...db._usersdata import getQuoraUserData
from ...utils.embeds._profileEmbed import profile_view
from ...utils.ui.profileUi import ProfileDropdownView


class UserProfile(commands.Cog):
    """class to generate general commands for bot

    Args:
        None
    Inherits:
        Inherits discord.ext.commands.Cog
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @discord.app_commands.command(name='profile',
                                  description='Fetches the profile')
    @discord.app_commands.describe(member="mention the user",
                                   username="Give your Quora Username or Link")
    async def profile(self,
                      interaction: discord.Interaction,
                      member: Optional[discord.Member],
                      username: Optional[str]):
        member = member if member is not None else interaction.user
        username = username if username is not None else 'Saurabh-Vishwakarma-228'
        userDataProfile, userDataAnswers, userDataTopic = await getQuoraUserData(username)
        embed = profile_view(member, userDataProfile, self.bot)
        view = ProfileDropdownView(
            interaction, self.bot, userDataProfile, userDataAnswers, userDataTopic)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(UserProfile(bot))
