import discord


class _ProfileDropdown(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(
            label="General Profile",
            description="Shows Profile of the user"
        ),
            discord.SelectOption(
            label="Profile Picture",
            description="Shows Profile Picture of the user"
        ),
            discord.SelectOption(
            label="Profile Bio",
            description="Shows Bio of the user"
        ),
            discord.SelectOption(
            label="Latest Answers",
            description="Shows the latest Answers by users"
        ),
            discord.SelectOption(
            label="Knows about",
            description="Shows about user"
        )]
        super().__init__(placeholder='More',
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.message.edit(embed=discord.Embed(title='bahaha'))
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


class ProfileDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(_ProfileDropdown())
