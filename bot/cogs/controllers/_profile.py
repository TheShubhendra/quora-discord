import discord
from discord.ext import commands
from typing import Optional


class UserProfile(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @discord.app_commands.command(name='profile', description='Fetches the profile')
    @discord.app_commands.describe(member="mention the user")
    async def profile(self, interaction: discord.Interaction, member: Optional[discord.Member]):
        member = member if member is not None else interaction.user
        await interaction.response.send_message(f'ok I got {member.display_name}')


async def setup(bot) -> None:
    await bot.add_cog(UserProfile(bot))
