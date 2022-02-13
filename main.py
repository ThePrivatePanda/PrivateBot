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
    "cogs.owner.guild_logger"
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
            exc = f"{type(e).__name__,}: {e}"
            print(f"Failed to load extension {extension}\n{exc}")

    # bot vars
    bot.prefix = config.prefix
    bot.owner_id = config.owner_id
    bot.appeal_server_invite = config.appeal_server_invite
    bot.main_server_invite = config.main_server_invite
    bot.afk_ignored_channels = []
    bot.session = aiohttp.ClientSession()
    bot.listening_channels = config.crosstalk
    bot.kucoin_api_key = config.kucoin_api_key
    bot.kucoin_api_secret = config.kucoin_api_secret
    bot.kucoin_api_passphrase = config.kucoin_api_passphrase

    bot.wait_until_ready()
    bot.home_server = bot.get_guild(int(config.home_server))
    bot.guild_logger = await bot.fetch_channel(config.guild_logger)
    bot.message_logger = await bot.fetch_channel(config.message_logger)

    # dbs
    bot.db = await aiosqlite.connect("dbs/db.sqlite3")
    await bot.db.execute(
        "CREATE TABLE IF NOT EXISTS afk (id bigint PRIMARY KEY, msg str)"
    )
    
bot.loop.create_task(my_startup_function())
bot.run(config.token)