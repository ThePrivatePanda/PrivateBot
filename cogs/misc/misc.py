import nextcord
from nextcord.ext import commands

import re

class Misc(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='dm')
    async def dm_(ctx, user: nextcord.User):
        try:
            await user.send("hi")
        except Exception as e:
            await ctx.send(e)
    
    @commands.group()
    async def emoji(self, ctx):
        pass

    @emoji.command(name="steal", hidden=True, aliases=['s'])
    async def emoji_steal(self, ctx, index: int = 0, guild: nextcord.Guild = None):
        if not ctx.message.reference:
            return await ctx.send('You referended no message to steal emotes from.')

        if not guild:
            if ctx.author.id != self.bot.owner_id:
                return await ctx.reply("You Need to give an guild id in which the stolen emote will be uploaded.")

        custom_emoji = re.compile(r"<a?:[a-zA-Z0-9_]+:[0-9]+>")
        emojis = custom_emoji.findall(ctx.message.reference.resolved.content)
        if not emojis:
            return await ctx.send("No emojis were found in the message you referenced.")

        try:
            emoji = await commands.PartialEmojiConverter().convert(ctx, emojis[index-1])
        except IndexError:
            return await ctx.send(f"Emoji out of index {index}/{len(emojis)}!\nIndex must be lower or equal to {len(emojis)}")

        file = await emoji.read()
        if ctx.author.id == self.bot.owner_id:
            guild = self.bot.get_guild(self.bot.config["home_server"])

        emoji = await guild.create_custom_emoji(name=f"m_{emoji.name}", image=file, reason="stole an emoji kek")

        try:
            await ctx.message.add_reaction(emoji)
        except nextcord.NotFound:
            pass

def setup(bot):
    bot.add_cog(Misc(bot))