from discord_components import DiscordComponents, Button, Select, SelectOption
from quora import User as QuoraUser
from discord.ext.commands import CommandError


class User(QuoraUser):
    def profile(self, cache_exp=180):
        return super().profile(self, cache_exp=cache_exp)

    def knows_about(self, cache_exp=3600):
        return super().knows_about(self, cache_exp=cache_exp)

    def answers(self, cache_exp=300):
        return super().answers(self, cache_exp=cache_exp)


class ProfileHelper:
    def __init__(self, *args, **kwargs):
        self.select_options = [
            SelectOption(
                label="General Profile",
                value="profile",
            ),
            SelectOption(
                label="Profile Picture",
                value="pic",
            ),
            SelectOption(
                label="Profile Bio",
                value="bio",
            ),
            SelectOption(
                label="Latest Answers",
                value="answers",
            ),
            SelectOption(
                label="Knows about",
                value="knows",
            ),
        ]
        self.components = [
            Select(
                placeholder="Select sections",
                options=self.select_options,
            )
        ]

    async def _get_embed(self, user, view, language="en"):
        profile = await user.profile(language)
        if view == "profile":
            embed = self.embed.profile(profile)
        elif view == "pic":
            embed = self.embed.profile_pic(profile)
        elif view == "bio":
            embed = self.embed.profile_bio(profile)
        elif view == "answers":
            answers = await user.answers(language)
            embed = self.embed.answers(profile, answers)
        elif view == "knows":
            profile = await user.profile()
            knows_about = await user.knows_about(language)
            embed = self.embed.knows_about(profile, knows_about)
        else:
            raise ValueError(view)
        return embed

    async def _generate_view(self, ctx, username, view="general", language="en"):
        user = User(username)
        message = await ctx.send(
            embed=await self._get_embed(user, view, language),
            components=self.components,
        )
        while True:
            try:
                interaction = await self.bot.wait_for(
                    "select_option",
                    check=lambda i: i.message == message,
                    timeout=30,
                )
            except TimeoutError:
                await message.edit(
                    components=[
                        Select(
                            placeholder="Select sections",
                            options=self.select_options,
                            disabled=True,
                        )
                    ]
                )
                return
            except Exception as e:
                self.logger.exception(str(e))
                continue
            if (
                interaction.user != ctx.author
                and interaction.user.id != self.bot.owner_id
            ):
                await interaction.respond(
                    content="You are not allowed to interact with this message.",
                )
                continue
            selection = interaction.values[0]
            embed = await self._get_embed(user, selection, language)
            try:
                await interaction.message.edit(
                    embed=embed,
                    components=self.components,
                )
            except:
                self.logger.exception("Error")

    async def get_username(self, ctx, quora_username=None):
        if len(ctx.message.mentions) > 0:
            discord_id = ctx.message.mentions[0].id
            if not self.bot.db.does_user_exist(discord_id):
                raise CommandError(
                    f"No Quora profile found related to {ctx.message.mentions[0]}"
                )
            quora_username = self.bot.db.get_quora_username(discord_id)
        elif quora_username is None:
            if not self.bot.db.does_user_exist(ctx.author.id):
                raise CommandError(
                    "Either setup your profile first or pass a username with the command."
                )
            quora_username = self.bot.db.get_quora_username(ctx.author.id)
        return quora_username
