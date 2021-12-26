from nextcord.ext import commands
class ttt(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

def setup(bot):
    bot.add_cog(ttt(bot))
