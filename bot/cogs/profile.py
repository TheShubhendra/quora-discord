from discord.ext import commands


class Profile(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def profile(self, ctx):
		await ctx.send("Hmm")

def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
