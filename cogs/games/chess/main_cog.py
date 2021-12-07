from nextcord.ext import commands
from tortoise.models import Model
import nextcord
from nextcord.utils import utcnow
from tortoise import fields

class ChessTable(Model):
    white = fields.BigIntField(pk=True)
    black = fields.BigIntField()
    game_id = fields.TextField()
    white_latest_game = fields.TextField()

class MainCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def play(self, ctx, opponent: nextcord.User):
        """Challenges user to a match"""
        challenge_message = await self.bot.reply(f'Hey {opponent.mention()}!\n{ctx.author.mention()} has challenged you to a chess match! React to accept or deny.')
        await challenge_message.add_reaction('✅')
        await challenge_message.add_reaction('❎')

        def check(reaction, user):
            return user.id == opponent.id and str(reaction.emoji) == '✅'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
        except:
            return await ctx.send('The challenge timed out!')
        unique_id = f"{ctx.author.id}#{opponent.id}#{utcnow()}"
        row = await ChessTable.get_or_create(white=ctx.author.id, black=opponent.id, game_id=unique_id, white_latest_game=unique_id)

    # @commands.command()
    # async def move(self, ctx):

def setup(bot):
    bot.add_cog(MainCog(bot), models=".")

# @commands.command(name="set_nick")
# async def set_nick(self, ctx, nick):
#     if len(nick) > 16 or len(nick)  :
#         nickname = await CustomNick.get_or_create(user=ctx.author.id, defaults={'nick': 'Nonelol'})
#         nickname[0].nick = nick
#         await nickname[0].save()
#         return await ctx.send("Done.")
#     await ctx.send("Failed.")

# @commands.command(name="hi")
# async def hi_(self, ctx):
#     nickname = await CustomNick.get(user=ctx.author.id)
#     if not nickname:
#         return await ctx.reply(f'You dont have a custom nickname configured! Configure it with: `!!set_nick new_nick`')
#     await ctx.reply(f"Hey {nickname.nick}")
