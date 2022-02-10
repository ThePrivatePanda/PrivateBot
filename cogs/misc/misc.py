import nextcord
from nextcord.ext import commands

import re

class Misc(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='dm')
    async def dm_(ctx, user: nextcord.User, message: str="hihi"):
        try:
            await user.send(message)
        except Exception as e:
            await ctx.send(e)
    

def setup(bot):
    bot.add_cog(Misc(bot))