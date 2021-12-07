from nextcord.ext import commands
class ttt(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(name="test")
    async def test_(self, ctx, arg1, arg2, arg3):
        await self.bot.db.execute(f'INSERT INTO ttt (user, opponent, winloss) VALUES({arg1}, {arg2}, {arg3});')
        await self.bot.db.commit()
        await ctx.reply('Done')

    @commands.command(name='testv2')
    async def testv2_(self, ctx):
        cursor = await self.bot.db.execute('SELECT * FROM ttt')
        rows = await cursor.fetchall()
        await ctx.reply(rows)

def setup(bot):
    bot.add_cog(ttt(bot))
