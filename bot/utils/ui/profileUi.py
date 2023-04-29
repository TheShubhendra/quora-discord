import discord
import quora
from ...utils.embeds._profileEmbed import (
    profile_view,
    profile_pic_view,
    profile_bio_view,
    profile_answers_view,
    profile_topic_view,
)
from typing import Callable, Any, Coroutine
from discord.ext import commands


class _ProfileDropdown(discord.ui.Select):
    def __init__(
        self,
        bot: commands.Bot,
        messageInteraction: discord.Interaction,
        userDataProfile,
        userDataAnswers,
        userDataKnows
    ):
        super().__init__()
        self.bot = bot
        self.userDataProfile = userDataProfile
        self.userDataAnswers = userDataAnswers
        self.userDataKnows = userDataKnows
        self.messageInteraction = messageInteraction
        options = [
            discord.SelectOption(
                label="General Profile", description="Shows Profile of the user"
            ),
            discord.SelectOption(
                label="Profile Picture", description="Shows Profile Picture of the user"
            ),
            discord.SelectOption(
                label="Profile Bio", description="Shows Bio of the user"
            ),
            discord.SelectOption(
                label="Latest Answers", description="Shows the latest Answers by users"
            ),
            discord.SelectOption(label="Knows about",
                                 description="Shows about user"),
        ]
        super().__init__(placeholder="Make a Selection",
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.messageInteraction.user.id == interaction.user.id:
            match (self.values[0]):
                case "General Profile":
                    await interaction.response.edit_message(
                        embed=profile_view(
                            self.messageInteraction.user, self.userDataProfile, self.bot
                        ),
                    )
                case "Profile Picture":
                    await interaction.response.edit_message(
                        embed=profile_pic_view(
                            self.messageInteraction.user, self.userDataProfile, self.bot
                        )
                    )
                case "Profile Bio":
                    await interaction.response.edit_message(
                        embed=profile_bio_view(
                            self.messageInteraction.user, self.userDataProfile, self.bot
                        )
                    )

                case "Latest Answers":
                    await interaction.response.edit_message(
                        embed=profile_answers_view(
                            self.messageInteraction.user, self.userDataProfile, self.userDataAnswers, self.bot
                        )
                    )
                case "Knows about":
                    await interaction.response.edit_message(
                        embed=profile_topic_view(
                            self.messageInteraction.user, self.userDataProfile, self.userDataKnows, self.bot
                        )
                    )
            self.placeholder = self.values[0]
        else:
            await interaction.response.send_message(
                "You can't interact with this message", ephemeral=True
            )


class ProfileDropdownView(discord.ui.View):
    def __init__(
        self,
        messageInteraction: discord.Interaction,
        bot: commands.Bot,
        userDataProfile: quora.Profile,
        userDataAnswers: quora.Answer,
        userDataKnows: Callable,
    ):
        self.messageInteraction = messageInteraction
        super().__init__()
        self.timeout = 30

        # Adds the dropdown to our view object.
        self.add_item(
            _ProfileDropdown(
                bot, messageInteraction, userDataProfile, userDataAnswers, userDataKnows
            )
        )

    async def on_timeout(self) -> Coroutine[Any, Any, None]:
        await self.messageInteraction.edit_original_response(view=None)
        # await self.messageInteraction.response.edit_message(view=None)
        return await super().on_timeout()
