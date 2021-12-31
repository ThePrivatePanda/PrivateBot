from nextcord.ext import commands

class AFK(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_afk_users(self):
        return [i[0] for i in await (await self.bot.db.execute("SELECT id FROM afk")).fetchall()]

    async def get_afk_message(self, id):
        return (await (await self.bot.db.execute(f"SELECT msg FROM afk WHERE id IS {id}")).fetchone())[0]

    async def write_afk(self, id, message):
        await self.bot.db.execute(f"INSERT INTO afk (id, msg) VALUES({id}, {message})")

    async def remove_afk(self, id):
        await self.bot.db.execute(f"DELTE FROM afk WHERE id IS {id}")

    async def go_afk(self, ctx, message):
        if id in await self.get_afk_users():
            await self.remove_afk(ctx.author.id)
        await self.write_afk(ctx.author.id, message)

    @commands.command(name="afk")
    async def afk_(self, ctx, msg="For some reason."):
        try:
            if await self.go_afk(ctx, msg):
                await ctx.send(f"{ctx.author.mention} set afk with: {msg}")
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(AFK(bot))