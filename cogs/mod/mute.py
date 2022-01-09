from datetime import timedelta
from nextcord.ext import commands
import nextcord
from nextcord import Permissions

from nextcord import SlashOption
from nextcord.interactions import Interaction

from humanfriendly import parse_timespan as pt

class Mute(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def shh(self, stuff, member, time, reason): # Requires member intents
        myctx = self.bot.Wrap(stuff)

        if member.id == self.bot.user.id:
            return await myctx.send("Simply: No.")
        if member.id == myctx.author.id:
            return await myctx.send("Ask someone higher than you to ban you.")

        if  myctx.author.guild_permissions.moderate_members:
            return await myctx.send("You aren't allowed to so don't try to.")
        if member.top_role > myctx.author.top_role:
            return await myctx.send("You are not high enough in the role hierarchy to ban them.")

        try:
            time = int(pt(time))
        except:
            return await myctx.send(f"Failed to parse time.\nPass something like `4 days`, `2 hours`, `40 minutes`, `400 seconds` or something.\n(`400` only number defaults to seconds.)")

        datetime_instance = nextcord.utils.utcnow() + timedelta(seconds=time)
        muted_till = nextcord.utils.format_dt(datetime_instance, "F")

        await member.edit(timeout=datetime_instance, reason=reason)

        if self.bot.get_user_dm(member.id):
            await member.send(
                embed=nextcord.Embed(
                    title="You were muted!",
                    color=nextcord.Color.dark_red(),
                    inline=False
                    ).add_field(
                        name="**Info:**",
                        value=f"""
                        Muted in: {myctx.guild.name} ({myctx.guild.id})
                        Muted till: {muted_till}
                        Muted by: {myctx.author.mention} ({myctx.author.id})
                        """
                    ).add_field(
                        name="**Reason:**",
                        value=f"{reason}"
                    ).add_field(
                        name="**Appeal:**",
                        value=f"Join the [appeal server]({self.bot.appeal_server_invite})."
                    )
                )

        await myctx.send(embed=nextcord.Embed(
            title="Muted!",
            color=nextcord.Color.green(),
            inline=False
            ).add_field(
                name="**Info:**",
                value=f"""
                Muted user: {member.mention} ({member.id})
                Muted till: {muted_till}
                Muted by: {myctx.author.mention} ({myctx.author.id})
                """
            ).add_field(
                name="**Reason:**",
                value=f"{reason}"
            )
        )

    @commands.command(name="mute", aliases=["timeout"])
    async def mute_prefixd(self, ctx, member: nextcord.Member, time: str = "900", *, reason="No reason given."):
        await self.shh(ctx, member, time, reason)

    @nextcord.slash_command(name="mute")
    async def mute_slash(self,
        interaction: Interaction,
        member: nextcord.Member = SlashOption(name="member", description="which member to be muted?", required=True),
        time: str = SlashOption(name="time", description="For how long should the user be muted?", required=False, default=900),
        reason: str = SlashOption(name="reason", description="Why is the user muted?", required=False, default="No reason given.")
    ):
        await self.shh(interaction, member, time, reason)


def setup(bot):
    bot.add_cog(Mute(bot))
