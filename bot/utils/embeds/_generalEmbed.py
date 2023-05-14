import discord
from discord.ext import commands
from datetime import datetime


def feedbackEmbed(
    client: commands.Bot, interaction_user: discord.Member, feedback: str
) -> discord.Embed:
    """return feedback embed

    Args:
        name (str): name entered by the user in feedback model
        feedback (str): feedback given by the user in feedback model

    Returns:
        discord.Embed: return embed
    """
    embed = discord.Embed(colour=discord.Colour.red())
    embed.set_author(name="Quora", icon_url=client.user.avatar.url)
    embed.add_field(name="Feedback Recieved", value=feedback)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url if interaction_user.avatar else None,
    )
    return embed


def pingEmbed(
    client: commands.Bot, interaction_user: discord.Member, latency: int
) -> discord.Embed:
    embed = discord.Embed(title=f"Pong! {latency}ms", colour=discord.Colour.red())
    embed.set_author(name=f"Quora Bot", icon_url=client.user.avatar.url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url if interaction_user.avatar else None,
    )
    return embed


def registerEmbed(
    client: commands.Bot, interaction_user: discord.Member, username: str, found: bool
) -> discord.Embed:
    if found is None:
        title = "Improper url provided"
    else:
        title = f"User registered as {username}"
    embed = discord.Embed(title=title, colour=discord.Colour.red())
    embed.set_author(name=f"Quora Bot", icon_url=client.user.avatar.url)
    if found:
        embed.add_field(name="To View Profile", value="Use /profile")
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url if interaction_user.avatar else None,
    )
    return embed


def profileNotFound(
    client: commands.Bot, interaction_user: discord.Member
) -> discord.Embed:
    embed = discord.Embed(
        title="No profile found with this account",
        description="To register with Quora Bot use /register command",
        color=discord.Color.red(),
    )
    embed.set_author(name="Quora Bot", icon_url=client.user.avatar.url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text=interaction_user.display_name,
        icon_url=interaction_user.avatar.url if interaction_user.avatar else None,
    )
    return embed
