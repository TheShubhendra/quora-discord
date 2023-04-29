import discord
import traceback
from discord.ext import commands
from ..embeds._generalEmbed import feedbackEmbed


class Feedback(discord.ui.Modal, title='Feedback'):

    feedback = discord.ui.TextInput(
        label='Your feedback about Quora Bot?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=True,
        max_length=200,
    )

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {interaction.user.name}!', ephemeral=True)
        guild = self.bot.get_guild(self.bot.LOGGING_GUILD.id)
        channel = guild.get_channel(self.bot.LOGGING_CHANNEL.id)
        embed = feedbackEmbed(self.bot, interaction.user, self.feedback.value)
        await channel.send(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
