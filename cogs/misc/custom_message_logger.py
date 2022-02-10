from nextcord.ext import commands

class CustomMessageLogger(commands.Cog):
    def __init__(self, bot) -> None:
        self. bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        my_webhook = await self.bot.message_logger.create_webhook(
                    name=message.author.name,
                    avatar=(await message.author.avatar.read()),
                )
        await my_webhook.send(message.content)
        await my_webhook.delete()

def setup(bot):
    bot.add_cog(CustomMessageLogger(bot))