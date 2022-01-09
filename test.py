from nextcord import member
from nextcord.ext import commands
import nextcord
import config

bot = commands.Bot(
    command_prefix=".",
    intents=nextcord.Intents.all(),
)


@bot.event
async def on_ready():
    print(f"Logged in.")


@bot.command(name="test")
async def test_(ctx):
    print(ctx.author.top_role.icon)
    await ctx.message.delete()
    # thread = await ctx.message.create_thread(name="ff123sss")
    # await ctx.send(str(ctx.message.thread))
    # await ctx.send(str(thread))
    # await ctx.send(str(thread.message))


@bot.command(name="renameme")
@commands.is_owner()
async def rename_(ctx, *, args):
    try:
        await ctx.guild.me.edit(nick=args, reason="they asked me to")
    except Exception as e:
        return await ctx.reply(e)
    await ctx.reply("done sadly.")


@bot.event
async def on_message_edit(before, after):
    await after.channel.send(str(after.thread))


bot.run(config.token)
