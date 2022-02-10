import nextcord
from nextcord.ext import commands

import re


class Emote(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.group()
    async def emoji(self, ctx):
        pass

    @emoji.command(name="steal", aliases=["rob"])
    async def emoji_steal(self, ctx, index: int = 0, guild: nextcord.Guild = None, name=None):
        if not ctx.channel.permissions_for(ctx.author).manage_emojis:
            if not await self.bot.is_owner(ctx.author):
                return await ctx.send("You don't have permission to do that.")

        if not ctx.message.reference:
            return await ctx.send("You referended no message to steal emotes from.")

        if not guild:
            if ctx.author.id != self.bot.owner_id:
                return await ctx.reply(
                    "You Need to give an guild id in which the stolen emote will be uploaded."
                )
            else:
                guild = self.bot.home_server

        custom_emoji = re.compile(r"<a?:[a-zA-Z0-9_]+:[0-9]+>")
        emojis = custom_emoji.findall(ctx.message.reference.resolved.content)

        if not emojis:
            return await ctx.send("No emojis were found in the message you referenced.")

        try:
            emoji = await commands.PartialEmojiConverter().convert(
                ctx, emojis[index]
            )
        except IndexError:
            return await ctx.send(
                f"Emoji out of index {index}/{len(emojis)}!\nIndex must be lower or equal to {len(emojis)}"
            )

        name = name or emoji.name
        file = await emoji.read()

        emoji = await guild.create_custom_emoji(
            name=name, image=file, reason="stole an emoji kek"
        )

        try:
            await ctx.message.add_reaction(emoji)
        except Exception as e:
            await ctx.send(f"Failed to add emoji to message: {e}")
        await ctx.reply(f"Uploaded :{emoji.name}: with name: {emoji.name} to guild: {guild.name}")



def setup(bot):
    bot.add_cog(Emote(bot))
