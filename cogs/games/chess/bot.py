import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

# import cairosvg
import ChessGame as chessgame

import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '!!', intents=intents, status=discord.Status.online, activity=discord.Game(name="Playing Chess"))
client.remove_command("$help")

match_requests = []
matches = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def accept(ctx: discord.ext.commands.Context):
    """Accepts a user's request"""
    global match_requests
    global matches
    message = ctx.message

    found = False
    for request in match_requests:
        # we have found the request
        if request.players[1].id == message.author.id:
            svg = request.board_to_svg()
            print(request.board)
            with open('board.svg', 'w') as f:
                f.write(svg)
                cairosvg.svg2png(url='board.svg', write_to='board.png')
                fi = discord.File('board.png')
                await ctx.send('Challenge from <@{0.id}> has been accepted!'.format(request.players[0]))
                await ctx.send('It is <@{0.id}>\'s turn!'.format(request.player), file=fi)
            matches.append(request)
            match_requests.remove(request)
            found = True
    if not found:
        await ctx.send('No pending challenges!')

@client.command()
async def move(ctx: discord.ext.commands.Context):
    """Makes move"""
    global matches

    message = ctx.message
    move = message.content.split(' ')[1]

    found = False
    for match in matches:
        # we have found the match
        if match.player.id == message.author.id:
            found = True
            valid, result = match.make_move(move)
            winner = None
            draw = False
            if result is not None:
                if result == '1-0':
                    winner = match.player
                elif result == '0-1':
                    winner = match.players[match.moves % 2]
                elif result == '1/2-1/2':
                    draw = True
            if not valid:
                await ctx.send('Invalid move, \'{0}\''.format(move))
            else:
                svg = match.board_to_svg()
                with open('board.svg', 'w') as f:
                    f.write(svg)
                    cairosvg.svg2png(url='board.svg', write_to='board.png')
                    fi = discord.File('board.png')
                    m = 'It is now <@{0.id}>\'s turn!'.format(match.player)
                    if winner is not None:
                        m = '<@{0.id}> wins!'.format(winner)
                    elif draw is True:
                        m = 'The match was a draw!'
                    await ctx.send(m, file=fi)
            if result is not None:
                matches.remove(match)
    if not found:
        await ctx.send('No match currently.')

@client.command()
async def end(ctx: discord.ext.commands.Context):
    """Ends match, what a loser"""
    global matches

    message = ctx.message

    found = False
    for match in matches:
        # we have found the match
        if match.player.id == message.author.id:
            found = True
            matches.remove(match)
            await ctx.send('Match forfeited.')
    if not found:
        await ctx.send('No match currently.')

client.run("Nzc5NjM3NDQwMjkzODk2MTkz.X7jb8g.zAUNxQroo74UslcJqf5qsm7O9UU")