from nextcord.ext import commands


class Crosstalk(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message_crosstalk(self, message):
        if message.channel.id not in self.bot.listening_channels:
            return
        if message.author.bot:
            return
        for channel in self.bot.listening_channels:
            if message.channel.id == channel:
                pass
            else:
                channel = self.bot.get_channel(channel)
                my_webhook = await channel.create_webhook(
                    name=message.author.name,
                    avatar=(await message.author.avatar.read()),
                )
                await my_webhook.send(message.content)
                await my_webhook.delete()


def setup(bot):
    bot.add_cog(Crosstalk(bot))
