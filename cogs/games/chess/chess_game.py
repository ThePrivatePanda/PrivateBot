dark_empty = 0x32674b
light_empty = 0xe7e7e4
dark_moved = 0x6b9453
light_moved = 0xc8d7a2

import asyncio
import chess
from PIL import Image
import time

class Game:
    def __init__(self, ascii_board, white, black) -> None:
        self.board = ascii_board
        self.white = white
        self.black = black

def is_legal_move(move, board):
    if move in str(board.legal_moves):
        return 'SAN'
    elif chess.Move.from_uci(move) in str(list(board.legal_moves)):
        return 'UCI'
    return False

async def check_if_is_legal_move(move, board):
    await asyncio.to_thread(is_legal_move, move, board)

board = """r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R"""

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

bot.run('Nzc5NjM3NDQwMjkzODk2MTkz.X7jb8g.B9UQM7wau6OvpenILV4hkQErh2M')

# await ctx.send(file=discord.File(fp=output_buffer, filename="my_file.png"))