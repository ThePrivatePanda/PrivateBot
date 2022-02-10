from nextcord.ext import commands

class GuildLogger(commands.Cog):
    def __init__(self, bot) -> None:
        self. bot = bot
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.bot.guild_logger.send(f"Joined guild: {guild.name} and it has {guild.member_count} members. I can now see a total of {len(self.bot.guilds)} guilds and {len(self.bot.users)} users.")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.guild_logger.send(f"Removed from guild: {guild.name} and it had {guild.member_count} members. I can now see a total of {len(self.bot.guilds)} guilds and {len(self.bot.users)} users.")

def setup(bot):
    bot.add_cog(GuildLogger(bot))