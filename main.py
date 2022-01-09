import sys

sys.dont_write_bytecode = True

import aiohttp
import config
from datetime import datetime
import asyncio
import aiosqlite

from BotBase import BotBaseBot

import nextcord


cogs = ["Fun.animals", "misc.afk", "test.test", "test.regularcmd", "test.slashcmd"]


bot = BotBaseBot(
    command_prefix=config.prefix,
    intents=nextcord.Intents.all(),
    status=nextcord.Status.online,
    activity=nextcord.Game(name="Playing nothing."),
    help_command=None,
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.id} at {datetime.now()}!")


def arg_manager():
    if sys.argv and len(sys.argv) == 1:
        return [i for i in cogs]
    if sys.argv and len(sys.argv) == 3 and "--" in str(sys.argv):
        args = sys.argv
        del args[0]

    if "--load" in args:
        loadable = [
            i
            for i in [
                a.replace(",", "").replace(".py", "")
                for a in args[args.index("--load") + 1].split(" ")
            ]
        ]
    elif "--dontload" in args:
        loadable = [
            i
            for i in [
                i
                for i in [i.replace(".py", "") for i in cogs]
                if i
                not in [
                    i.replace(",", "").replace(".py", "")
                    for i in args[args.index("--dontload") + 1].split(" ")
                ]
            ]
        ]
    elif "--loadall" in args:
        loadable = [i for i in cogs]
    else:
        print("Unknwn flasg passed, exiting.")
        raise SystemExit
    return loadable


async def my_startup_function():
    # cogs
    loadable = arg_manager()
    loadable = [f"cogs.{i}" for i in loadable]
    for extension in loadable:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded extension {extension}")
        except Exception as e:
            exc = f"{type(e).__name__,}: {e}"
            print(f"Failed to load extension {extension}\n{exc}")

        bot.token = config.token
        bot.home_server = int(config.home_server)
        bot.appeal_server_invite = config.appeal_server_invite
        bot.main_server_invite = config.main_server_invite
        bot.afk_ignored_channels = []

    # dbs
    bot.db = await aiosqlite.connect("dbs/db.sqlite3")
    await bot.db.execute(
        "CREATE TABLE IF NOT EXISTS afk (id bigint PRIMARY KEY, msg str)"
    )

    async with aiohttp.ClientSession() as session:
        bot.session = session

        try:
            await bot.start(bot.token)
        except KeyboardInterrupt:
            raise SystemExit


asyncio.run(my_startup_function())
