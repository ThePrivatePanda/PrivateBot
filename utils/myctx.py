from nextcord import Interaction
from nextcord.ext.commands import Context

class MyCtx:
    def __init__(self, author, bot, channel, guild, message) -> None:
        self.author = author
        self.bot = bot
        self.channel = channel
        self.guild = guild
        self.message = message

async def make_ctx(stuff):
    if isinstance(stuff, Interaction):
        author = stuff.user
        bot = False

    elif isinstance(stuff, Context):
        author = stuff.author
        bot = stuff.bot
    else:
        return False

    return MyCtx(author, bot, stuff.channel, stuff.guild, stuff.message)



from typing import Union

from nextcord import Interaction, User, Member
from nextcord.ext.commands import Context

class WrappedShit:
    def __init__(self, wrap: Union[Interaction, Context]):
        self._wrap: Union[Interaction, Context] = wrap

        self._is_interaction = isinstance(self._wrap, Interaction)

    @property
    def author(self) -> Union[User, Member]:
        if self._is_interaction:
            return self._wrap.user

        return self._wrap.author

    @classmethod
    async def send(self)