import aiohttp
from config import token
startup_extensions = ["cogs.main_cog"]
from run import bot

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.id}!")

async def my_startup_function():
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded extension {extension}")
        except Exception as e:
            exc = f"{type(e).__name__,}: {e}"
            print(f"Failed to load extension {extension}\n{exc}")

    async with aiohttp.ClientSession() as session:
        bot.session = session
        bot.token = token
        try:
            await bot.start(bot.token)
        except KeyboardInterrupt:
            raise SystemExit
