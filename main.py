import sys
sys.dont_write_bytecode = True

import aiohttp
import config
from datetime import datetime
from run import bot

if sys.argv and len(sys.argv) == 3 and "--" in str(sys.argv):
    args = sys.argv
    del args[0]

cogs = ["fun.animals"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.id} at {datetime.now()}!")

@bot.command(name="guildname")
async def guildname_(ctx, name):
    await ctx.guild.edit(name=name)
    await ctx.send("Done.")

async def my_startup_function():
    if "--load" in args:
        loadable = [i for i in [a.replace(",", "").replace(".py", "") for a in args[args.index("--load")+1].split(" ")]]
    elif "--dontload" in args:
        loadable = [i for i in [i for i in [i.replace(".py", "") for i in cogs] if i not in [i.replace(",", "").replace(".py", "") for i in args[args.index("--dontload")+1].split(" ")]]]
    elif "--loadall" in args:
        loadable = [i for i in cogs]
    else:
        print("Unknwn flasg passed, exiting.")
        raise SystemExit

    loadable = [f"cogs/{i}.py" for i in loadable]
    for extension in loadable:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded extension {extension}")
        except Exception as e:
            exc = f"{type(e).__name__,}: {e}"
            print(f"Failed to load extension {extension}\n{exc}")


    async with aiohttp.ClientSession() as session:
        bot.session = session
        bot.token = config.token
        bot.home_server = int(config.home_server)

        try:
            await bot.start(bot.token)
        except KeyboardInterrupt:
            raise SystemExit
