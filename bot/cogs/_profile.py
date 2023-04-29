import discord
from discord.ext import commands
from typing import Optional
from ..db._usersdata import getQuoraUserData
from ..utils.embeds._profileEmbed import profile_view
from ..utils.ui.profileUi import ProfileDropdownView
from ..utils.parser.usernameParser import getQuoraUsername


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

    @discord.app_commands.command(name='profile',
                                  description='Fetches the profile')
    @discord.app_commands.describe(member="mention the user",
                                   username="Give your Quora Username or Link")
    async def profile(self,
                      interaction: discord.Interaction,
                      member: Optional[discord.Member],
                      username: Optional[str]):

        member = member if member is not None else interaction.user
        _username = None
        if username is None:
            _username = self.bot.db.getQuoraUsername(member.id)
        try:
            if username is None and _username is None:
                await interaction.response.send_message("profile not found!!")
            else:
                username = username if username else _username
                userDataProfile, userDataAnswers, userDataKnows = await getQuoraUserData(username)
                view = ProfileDropdownView(
                    interaction, self.bot, userDataProfile, userDataAnswers, userDataKnows)
                embed = profile_view(member, userDataProfile, self.bot)
                await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            print(e)


async def setup(bot) -> None:
    await bot.add_cog(UserProfile(bot))

    # if _username is None:
    #     self.bot.db.addQuoraUsername(discord_id=member.id,
    #                                  quora_username=username,
    #                                  discord_username=member.name,
    #                                  follower_count=userDataProfile.followerCount)
