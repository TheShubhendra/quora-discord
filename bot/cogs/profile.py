from discord.ext import commands
from profiles.quora import User

class Profile(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def profile(self, ctx, arg):
		await ctx.send(User(arg))

def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
