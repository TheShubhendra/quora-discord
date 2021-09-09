from asyncio import TimeoutError
from discord_components import (
    Button,
    Select,
    SelectOption,
    ButtonStyle,
)
from quora.user import subdomains
from quora.exceptions import ProfileNotFoundError
from discord.ext.commands import CommandError
from bot.utils import extract_quora_username


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
        try:
            profile = await user.profile(language=language)
        except ProfileNotFoundError:
            raise CommandError(
                f"No profile found with the username {user.username}\
on Quora {subdomains[language]}"
            )
        if view == "profile":
            embed = self.embed.profile(profile)
        elif view == "pic":
            embed = self.embed.profile_pic(profile)
        elif view == "bio":
            embed = self.embed.profile_bio(profile)
        elif view == "answers":
            answers = await user.answers(language=language)
            embed = self.embed.answers(profile, answers)
        elif view == "knows":
            profile = await user.profile(language=language)
            knows_about = await user.knows_about(language=language)
            embed = self.embed.knows_about(profile, knows_about)
        else:
            raise ValueError(view)
        return embed

    async def _generate_view(
        self,
        ctx,
        user_or_username,
        view="general",
        language="en",
    ):
        if isinstance(user_or_username, str):
            user = self.bot.get_quora(username)
        elif user_or_username is None:
            return
        else:
            user = self.bot.get_quora(user_or_username.quora_username)
            language = user_or_username.profiles[0]. language
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
                    content="You are not allowed\
to interact with this message.",
                )
                continue
            selection = interaction.values[0]
            embed = await self._get_embed(user, selection, language)
            try:
                await interaction.message.edit(
                    embed=embed,
                    components=self.components,
                )
            except Exception:
                self.logger.exception("Error")

    async def get_username(self, ctx, quora_username=None):
        if len(ctx.message.mentions) > 0:
            discord_id = ctx.message.mentions[0].id
            if not self.bot.db.does_user_exist(discord_id):
                raise CommandError(
                    f"No Quora profile found\
related to {ctx.message.mentions[0]}"
                )
            return self.bot.db.get_user(discord_id)
        elif quora_username is None:
            if not self.bot.db.does_user_exist(ctx.author.id):

                async def callback(inter):
                    await self._setprofile_view(ctx)

                await ctx.send(
                    embed=self.embed.get_default(
                        title="Profile not found",
                        description="No Quora profile \
linked with your account found.\
Please link your profile first or pass any username with the command.",
                    ),
                    components=[
                        self.bot.components_manager.add_callback(
                            Button(
                                style=ButtonStyle.green,
                                label="Link Quora profile",
                            ),
                            callback,
                        )
                    ],
                )
                return
            return self.bot.db.get_user(ctx.author.id)
        if quora_username is not None:
            return quora_username
        else:
            return

    async def _setprofile_view(self, ctx, username=None, manage=True):
        if manage and self.bot.db.does_user_exist(discord_id=ctx.author.id):
            await self._manageprofile(ctx)
            return
        if username is None:
            message = await ctx.send(
                embed=self.embed.get_default(
                    title="Set Profile",
                    description="Please send your Quora username or profile link in order to link your profile with the bot.",
                )
            )
            while True:
                try:
                    msg = await self.bot.wait_for(
                        "message",
                        check=lambda x: x.author == ctx.author
                        and x.channel == message.channel,
                        timeout=20,
                    )
                except TimeoutError:
                    await ctx.send(
                        embed=self.embed.get_default(
                            title="Time out",
                            description=f"{ctx.author.mention} you failed to reply with your Quora username or profile link in given time",
                        )
                    )
                    return
                username = extract_quora_username(msg.content)
                if username is None:
                    await ctx.send("Please send valid username")
                    continue
                else:
                    break

        embed = self.embed.get_default(
            title="Set Profile",
            description="Please select the language",
        )
        message = await ctx.send(
            embed=embed,
            components=[
                Select(
                    placeholder="Select language",
                    options=[
                        SelectOption(label=name, value=value)
                        for value, name in subdomains.items()
                    ],
                )
            ],
        )
        try:
            interaction = await self.bot.wait_for(
                "select_option",
                check=lambda x: x.message == message and x.user == ctx.author,
                timeout=30,
            )
        except TimeoutError:
            await message.edit(
                embed=embed,
                components=[
                    Select(
                        placeholder="Selection time out",
                        disabled=True,
                        options=[SelectOption(label="raw", value="raw")],
                    )
                ],
            )
            return
        language = interaction.values[0]
        try:
            await self.bot.get_quora(username).profile(language=language)
        except ProfileNotFoundError:

            async def retry(inter):
                await self._setprofile_view(ctx)

            await message.edit(
                embed=self.embed.get_default(
                    title="Profile not found",
                    description=f"No profile found with the username {username} on Quora {subdomains[language]}",
                ),
                components=[
                    self.bot.components_manager.add_callback(
                        Button(
                            style=ButtonStyle.blue,
                            label="Retry",
                        ),
                        retry,
                    )
                ],
            )
            return
        await self._setprofile(ctx.author, username, language)
        await message.edit(
            embed=self.bot.embed.get_default(
                title="Profile linked successfully",
                description=f"{ctx.author.mention}'s Quora account with the username {username} has been successfully linked with the bot",
            ),
            components=[],
        )

    async def _setprofile(self, user, username, language="en"):
        profile = await self.bot.get_quora(username).profile(language=language)
        user_id = user.id
        user = self.bot.db.add_user(
            user_id,
            user.name + "#" + str(user.discriminator),
            username,
            profile.followerCount,
        )
        self.bot.db.add_profile(user, language=language)

    async def _manageprofile(
        self,
        ctx,
        action=None,
    ):
        user = self.bot.db.get_user(discord_id=ctx.author.id)
        if user is None:
            return
        linked_languages = ""
        for i,profile in enumerate(user.profiles):
            linked_languages+=f"{i+1}. {subdomains[profile.language]}\n" 
        embed = self.embed.get_default(
            title="Profile Manager",
            description=f"Your Quora account with username {user.quora_username} is linked in following languages.\n"
            + linked_languages,
        )

        async def callback(inter):
            if inter.custom_id == "add_lang":
                await self._addlang_view(user, inter.message)
            elif inter.custom_id == "change_username":
                await self._setprofile_view(ctx, manage=False)
            elif inter.custom_id == "unlink":
                await self._unlink_view(user, inter.message)

        await ctx.send(
            embed=embed,
            components=[
                [
                    self.bot.components_manager.add_callback(
                        Button(
                            style=ButtonStyle.green,
                            label="Add other languages",
                            custom_id="add_lang",
                        ),
                        callback,
                    ),
                    self.bot.components_manager.add_callback(
                        Button(
                            style=ButtonStyle.blue,
                            label="Change username",
                            custom_id="change_username",
                        ),
                        callback,
                    ),
                    self.bot.components_manager.add_callback(
                        Button(
                            style=ButtonStyle.red,
                            label="Unlink",
                            custom_id="unlink",
                        ),
                        callback,
                    ),
                ]
            ],
        )

    async def _addlang_view(self, user, message):
        await message.edit(
            embed=self.embed.get_default(
                title="Add more languages",
                description="Select the language to add",
            ),
            components=[
                Select(
                    placeholder="Select language",
                    options=[
                        SelectOption(label=name, value=value)
                        for value, name in subdomains.items()
                    ],
                )
            ],
        )
        while True:
            try:
                interaction = await self.bot.wait_for(
                    "select_option",
                    check=lambda x: x.message == message
                    and x.user.id == int(user.discord_id),
                    timeout=30,
                )
            except TimeoutError:
                await message.edit(
                    embed=self.bot.embed.get_default(
                        title="Request time out",
                        description="You couldn't respond properly in given time.",
                    ),
                    components=[
                        Select(
                            placeholder="Selection time out",
                            disabled=True,
                            options=[SelectOption(label="raw", value="raw")],
                        )
                    ],
                )
                return
            language = interaction.values[0]
            if language in list(map(lambda x: x.language, user.profiles)):
                await interaction.respond(
                   content= "This language profile is already linked with Your account"
                    )
                continue
            try:
                await self.bot.get_quora(user.quora_username).profile(language=language)
            except ProfileNotFoundError:
                await interaction.respond(
                    content=f"No Quora profile found on Quora {language} with username {user.quora_username}"
                )
                continue
            break
        self.bot.db.add_profile(user, language=language)
        await message.edit(
            embed=self.bot.embed.get_default(
                title="Language Added",
                description=f"Quora {language} profile has been successfully linked to your account.",
            ),
            components=[],
        )

    async def _unlink_view(self, user, message):
        async def callback(inter):
            if inter.custom_id == "no":
                await inter.message.edit(
                    embed=self.bot.embed.get_default(
                        title="Account Manager",
                        description="Glad :) to hear that you wished to keep your account linked with the bot.\nKeep Quoring!!",
                    ),
                    components=[],
                )
            elif inter.custom_id == "yes":
                #  await self._unlink(user) will be used in future commits
                await inter.message.edit(
                    embed=self.embed.get_default(
                        title="Profile removed",
                        description="Your profile has been removed successfully.",
                    ),
                    components=[],
                )

        await message.edit(
            embed=self.embed.get_default(
                title="Remove account",
                description="Are you really want to unlink your Quora account with the bot",
            ),
            components=[
                [
                    self.bot.components_manager.add_callback(
                        Button(
                            style=ButtonStyle.green,
                            label="No, Keep my account",
                            custom_id="no",
                        ),
                        callback,
                    ),
                    self.bot.components_manager.add_callback(
                        Button(
                            style=ButtonStyle.red,
                            label="Yes, please remove it!",
                            custom_id="yes",
                        ),
                        callback,
                    ),
                ]
            ],
        )
