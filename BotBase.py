from nextcord.abc import GuildChannel
from nextcord.ext import commands
from nextcord import Guild, Member, User, DMChannel
from nextcord.ext import commands

import aiohttp
import config
import aiosqlite


class BotBaseBot(commands.Bot):
    async def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # bot vars
        self.prefix = config.prefix
        self.home_server = self.get_guild(int(config.home_server))
        self.guild_logger = await self.fetch_channel(config.guild_logger)
        self.message_logger = await self.fetch_channel(config.message_logger)
        self.owner_id = config.owner_id
        self.appeal_server_invite = config.appeal_server_invite
        self.main_server_invite = config.main_server_invite
        self.afk_ignored_channels = []
        self.session = aiohttp.ClientSession()
        self.listening_channels = config.crosstalk
        self.kucoin_api_key = config.kucoin_api_key
        self.kucoin_api_secret = config.kucoin_api_secret
        self.kucoin_api_passphrase = config.kucoin_api_passphrase

        # dbs
        self.db = await aiosqlite.connect("dbs/db.sqlite3")
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS afk (id bigint PRIMARY KEY, msg str)"
        )


    async def get_or_fetch_guild(self, guild_id: int) -> Guild:
        """Looks up a guild in cache or fetches if not found."""
        guild = self.get_guild(guild_id)
        if guild:
            return guild

        try:
            guild = await self.fetch_guild(guild_id)
        except:
            return False
        return guild

    async def get_or_fetch_user(self, user_id: int) -> User:
        """Looks up a user in cache or fetches if not found."""
        user = self.get_user(user_id)
        if user:
            return user
        try:
            user = await self.fetch_user(user_id)
        except:
            return False
        return user

    async def get_or_fetch_member(self, guild_id: int, member_id: int) -> Member:
        """Looks up a member in cache or fetches if not found."""

        guild = await self.get_or_fetch_guild(guild_id)
        if not guild:
            return await self.get_or_fetch_user(member_id)

        member = guild.get_member(member_id)

        if member is not None:
            return member

        try:
            member = await guild.fetch_member(member_id)
        except:
            member = await self.get_or_fetch_user(member_id)

        return member

    async def get_or_fetch_channel(self, channel_id: int) -> GuildChannel:
        """Looks up a channel in cache or fetches if not found."""
        channel = self.get_channel(channel_id)
        if channel:
            return channel

        try:
            channel = await self.fetch_channel(channel_id)
        except:
            return False

        return channel

    async def get_user_dm(self, user_id: int, *args, **kwargs) -> DMChannel:
        try:
            user = await self.get_or_fetc_user(user_id)
            if user:
                try:
                    await user.send(
                        *args, **kwargs
                    )
                    return True
                except:
                    return False
        except:
            return False
        return False

    async def WrapStuff(self, stuff):
        pass
