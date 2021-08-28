from discord.ext.commands import CommandError


class NotBotModerator(CommandError):
    """Moderator only command."""

    pass
