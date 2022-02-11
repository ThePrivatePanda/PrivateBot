import sys
import traceback

sys.dont_write_bytecode = True

import aiohttp
import config
from datetime import datetime
import aiosqlite

from BotBase import BotBaseBot

import nextcord


cogs = [
    "cogs.Fun.animals",
    # "cogs.misc.afk",
    "jishaku",
    "cogs.misc.emote",
    "cogs.Fun.activities",
    "cogs.misc.crosstalk",
]


bot = BotBaseBot(
    command_prefix=config.prefix,
    intents=nextcord.Intents.all(),
    status=nextcord.Status.online,
    activity=nextcord.Game(name="Playing nothing."),
    help_command=None,
    owner_ids=config.owners,
)


@bot.command(name="help")
async def help(ctx):
    return await ctx.send("Soon.")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} at {datetime.now()}!")


async def my_startup_function():
    # cogs
    for extension in cogs:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded extension {extension}")
        except Exception as e:
            traceback.format_exc()
            exc = f"{type(e).__name__,}: {e}"
            print(f"Failed to load extension {extension}\n{exc}")

bot.loop.create_task(my_startup_function())
bot.run(config.token)
