from discord.ext import commands
import discord
from ..utils.ui.feedbackUi import Feedback
from ..utils.embeds._generalEmbed import pingEmbed, registerEmbed
from ..utils.parser.usernameParser import getQuoraUsername
from quora import User


class InfoAndFeedbackCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @discord.app_commands.command(
        name="feedback", description="Send feedback to the developers!"
    )
    async def feedback(self, interaction: discord.Interaction):
        # Send the modal with an instance of our `Feedback` class
        # Since modals require an interaction, they cannot be done as a response to a text command.
        # They can only be done as a response to either an application command or a button press.
        await interaction.response.send_modal(Feedback(self.bot))

    @discord.app_commands.command(name="ping", description="Replies with Pong!")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000, 1)
        await interaction.response.send_message(
            embed=pingEmbed(self.bot, interaction.user, latency)
        )

    @discord.app_commands.command(
        name="register", description="register the quora user!"
    )
    @discord.app_commands.describe(url="Provide url of your Quora profile")
    async def register(self, interaction: discord.Interaction, url: str):
        username = getQuoraUsername(url)
        url_check = False
        if not self.bot.db.checkUserExistence(interaction.user.id):
            try:
                quorauser = User(username=username)
                userProfile = await quorauser.profile()
            except Exception as e:
                await interaction.response.send_message(
                    "improper url has been provided", ephemeral=True
                )
                self.bot.logging(e)
                return
            self.bot.db.addQuoraUsername(
                discord_id=interaction.user.id,
                quora_username=username,
                discord_username=interaction.user.name,
                follower_count=userProfile.followerCount,
            )
            url_check = True
            await interaction.response.send_message(
                embed=registerEmbed(self.bot, interaction.user, username, url_check)
            )
        else:
            await interaction.response.send_message(
                "User is already registered", ephemeral=True
            )

    @discord.app_commands.command(name="remove", description="Removes Quora Profile")
    async def remove(self, interaction: discord.Interaction):
        if self.bot.db.checkUserExistence(interaction.user.id):
            self.bot.db.removeUserExistence(interaction.user.id)
            await interaction.response.send_message("Profile removed", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Profile is not registered", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(InfoAndFeedbackCommands(bot))
