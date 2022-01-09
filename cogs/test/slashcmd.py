import nextcord
from nextcord.ext import commands

class slashcmd(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="mute", guild_ids=[0])
    async def cmdcmd(self, interaction: nextcord.Interaction):
        await interaction.send("no")

def setup(bot):
    bot.add_cog(slashcmd(bot))