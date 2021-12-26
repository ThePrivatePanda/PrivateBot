import nextcord
from nextcord.ext import commands
from nextcord.utils import utcnow

from tortoise.models import Model
from tortoise import fields

import chess

class ChessTable(Model):
    white = fields.BigIntField(pk=True)
    black = fields.BigIntField()
    game_id = fields.TextField()
    white_latest_game = fields.TextField()

class MainCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def create_board_image(ascii_board):
        before = time.time()
        ascii_board = str(ascii_board).replace(' ', '').replace('\n', '')
        board = Image.open('imgs/basic_board.png').convert('RGBA')
        coo = [(a,b) for a in range(0,8) for b in range (0,8)]
        for i in range(len(ascii_board)):
            if ascii_board[i] == '.':
                piece = None
            elif ascii_board[i] == 'r':
                piece = 'br'
            elif ascii_board[i] == 'n':
                piece = 'bn'
            elif ascii_board[i] == 'b':
                piece = 'bb'
            elif ascii_board[i] == 'q':
                piece = 'bq'
            elif ascii_board[i] == 'k':
                piece = 'bk'
            elif ascii_board[i] == 'p':
                piece = 'bp'
            elif ascii_board[i] == 'R':
                piece = 'wr'
            elif ascii_board[i] == 'N':
                piece = 'wn'
            elif ascii_board[i] == 'B':
                piece = 'wb'
            elif ascii_board[i] == 'Q':
                piece = 'wq'
            elif ascii_board[i] == 'K':
                piece = 'wk'
            elif ascii_board[i] == 'P':
                piece = 'wp'
            if piece is not None:
                piece = Image.open(f'imgs/{piece}.png').convert('RGBA')
                board.paste(piece, (int(coo[i][1]*50), int(coo[i][0]*50)), piece)
        print(time.time()-before)
        output_buffer = BytesIO()
        board.save(output_buffer, "jpg")
        output_buffer.seek(0)
        return output_buffer

    async def get_board(ascii_board):
        await asyncio.to_thread(create_board_image, ascii_board)

    def is_legal_move(move, board):
        if move in str(board.legal_moves):
            return 'SAN'
        elif chess.Move.from_uci(move) in str(list(board.legal_moves)):
            return 'UCI'
        return False
    
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
