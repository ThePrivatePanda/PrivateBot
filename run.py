from nextcord_tortoise import attach_argparse_group
import argparse
parser = argparse.ArgumentParser(description="Discord Bot")
attach_argparse_group(parser)
args = parser.parse_args()

import BotBase
TORTOISE_CONFIG = {
  "connections": {
    "default": "sqlite://db//db.sqlite3"
    }
}

from config import prefix
import asyncio
import nextcord
bot = BotBase.BotBaseBot(command_prefix=prefix, intents=nextcord.Intents.all(), status=nextcord.Status.online, activity=nextcord.Game(name="Playing Chess"), help_command=None, tortoise_config=TORTOISE_CONFIG)

if args.aerich:
    from nextcord_tortoise.aerich import run_aerich  # Done to avoid importing Aerich when unused
    run_aerich(bot, args)
else:
    from main import my_startup_function
    asyncio.run(my_startup_function())