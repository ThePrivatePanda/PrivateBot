from nextcord.abc import GuildChannel
from nextcord.ext import commands
from nextcord import Guild, Member, User
from nextcord_tortoise import Bot as TortoiseBot

class BotBaseBot(TortoiseBot):
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
