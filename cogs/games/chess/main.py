import nextcord
from nextcord.ext import commands
from ChessGame import ChessGame
bot = commands.Bot(command_prefix = "!!", intents=nextcord.Intents.all(), status=nextcord.Status.online, activity=nextcord.Game(name="Playing Chess"), help_command=None)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def play(ctx, opponent: nextcord.User):
    """Challenges user to a match"""
    challenge_message = await bot.reply(f'Hey {opponent.mention()}!\n{ctx.author.mention()} has challenged you to a chess match! React to accept or deny.')
    await challenge_message.add_reaction('✅')
    await challenge_message.add_reaction('❎')

    def check(reaction, user):
        return user.id == opponent.id and str(reaction.emoji) == '✅'

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)
    except:
        return await ctx.send('The challenge timed out!')

    game = ChessGame(ctx.author.id, opponent.id)