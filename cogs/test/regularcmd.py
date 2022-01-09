from nextcord.ext import commands

class regularcmd(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def cmdcmd(self, ctx):
        await ctx.send("no")

def setup(bot):
    bot.add_cog(regularcmd(bot))