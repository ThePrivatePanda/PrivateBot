from nextcord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.message.create_thread(name="ff123sss")
        print(ctx.message.thread)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        print(after.thread)

def setup(bot):
    bot.add_cog(Test(bot))