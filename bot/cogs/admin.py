from typing import Optional
from discord.ext import commands
from discord import File, User, Embed
from decouple import config
import heroku3
import asyncio
import os

from ..utils.exceptions import NotBotModerator


HEROKU_API_KEY = config("HEROKU_API_KEY", None)
HEROKU_APP_NAME = config("HEROKU_APP_NAME", None)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.heroku_client = heroku3.from_key(HEROKU_API_KEY)
        self.heroku_app = self.heroku_client.app(HEROKU_APP_NAME)

    @commands.command(
        aliases=["l", "log"],
        hidden=True,
    )
    async def logs(self, ctx: commands.Context):
        await ctx.trigger_typing()
        logs = self.heroku_app.get_log()
        if len(logs) > 1000:
            with open("logs.txt", "w") as log:
                log.write(logs)
            with open("logs.txt", "rb") as log:
                await ctx.send(
                    file=File(log, filename="Heroku logs"),
                    delete_after=60,
                )
        else:
            await ctx.send(logs, delete_after=60)
        await asyncio.sleep(3)
        os.remove("logs.txt")

    @commands.command(hidden=True)
    async def setp(
        self,
        ctx: commands.Context,
        user: User,
        username: str,
        lang: Optional[str] = "en",
    ):
        cog = self.bot.get_cog("Profile")
        await cog._setprofile(user, username, lang)
        await ctx.send(
            embed=self.bot.embed.get_default(
                title="Profile linked successfully",
                description=f"{user.mention}'s Quora {lang} account with the username {username} has been successfully linked with the bot",
            ),
        )

    @commands.command(hidden=True)
    async def guilds(self, ctx: commands.Context):
        guilds = self.bot.guilds
        txt = "```\n"
        for i in guilds:
            txt += f"{i.id}  : {i}\n"
        await ctx.reply(txt + "```", delete_after=30)

    @commands.command(hidden=True)
    async def restart(self, ctx: commands.Context):
        await ctx.reply("Going to restart the bot.")
        self.heroku_app.restart()

    async def cog_check(self, ctx: commands.Context):
        if ctx.bot.is_moderator(ctx.author):
            return True
        else:
            raise NotBotModerator(
                "This command can be used by owner or a bot moderator only."
            )
            return False

    async def get_channel(self, guild):
        if guild.system_channel:
            if guild.system_channel.permissions_for(guild.me).send_messages:
                return guild.system_channel
        messages = []
        for i in guild.text_channels:
            if i.last_message_id is None:
                continue
            msg = await i.fetch_message(i.last_message_id)
            messages.append(msg)
        channels = list(
            map(
                lambda m: m.channel,
                sorted(messages, key=lambda i: i.created_at, reverse=True),
            )
        )
        for channel in channels:
            perms = channel.permissions_for(channel.guild.me)
            if perms.send_messages:
                return channel

    @commands.Cog.listener(name="on_member_remove")
    async def leave(self, member):
        if not self.bot.is_admin(member):
            return
        channel = await self.get_channel(member.guild)
        txt = "I am sorry to say \
that my developer Shubhendra Kushwaha \
didn't feel good here and left the server \n(╥﹏╥)."
        try:
            embed = Embed(
                title="Shubhendra Sir left",
                description=txt,
            )
            embed.set_image(
                url="https://cdn.pixabay.com/photo/2017/11/26/15/16/smiley-2979107_640.jpg",
            )
            await channel.send(
                embed=embed,
            )
            await self.bot.log(f"Sent Admin leave message to {channel} {channel.guild}")
        except Exception as e:
            await self.bot.log(e)

    @commands.Cog.listener(name="on_member_join")
    async def join(self, member):
        if not self.bot.is_admin(member):
            return
        channel = await self.get_channel(member.guild)
        txt = f"I'm so excited to tell that my developer {member.mention} just joined this Server. I'm feeling so lucky to have him here.(๑♡⌓♡๑)"
        try:
            embed = Embed(
                title="Shubhendra sir joined",
                description=txt,
            )
            embed.set_image(
                url="https://cdn.pixabay.com/photo/2015/10/16/19/18/balloon-991680_640.jpg",
            )
            await channel.send(
                embed=embed,
            )
            await self.bot.log(f"Sent Admin join message to {channel} {channel.guild}")
        except Exception as e:
            await self.bot.log(e)


def setup(bot):
    cog = Admin(bot)
    bot.add_cog(cog)
