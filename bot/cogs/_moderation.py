from discord import app_commands
from discord.ext import commands
import discord


class OnlyGuildsCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="get_users_lists",
        description="Get the list of all users who are register to Quora Bot",
    )
    async def get_users_list(self, interaction: discord.Interaction):
        data = self.bot.db.getAllQuorans()

        await interaction.response.send_message(data)


async def setup(bot: commands.Bot):
    await bot.add_cog(OnlyGuildsCommands(bot))
