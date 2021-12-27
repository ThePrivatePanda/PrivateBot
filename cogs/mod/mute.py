from datetime import timedelta
from nextcord.ext import commands
import nextcord

from nextcord import SlashOption
from nextcord.flags import Intents
from nextcord.interactions import Interaction

from humanfriendly import parse_timespan as pt

class Mute(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def shh(self, myctx, member, time, reason): # Requires member intents
        try:
            time = pt(time)
        except Exception as e:
            return await myctx.send(f"Failed to parse time with error {e}")
        datetime_instance = nextcord.utils.utcnow() + timedelta(seconds=time)
        muted_till = nextcord.utils.format_dt(datetime_instance, "F")
        await member.edit(timeout=datetime_instance, reason=reason)
        if isinstance(myctx, Interaction):
            author = myctx.user
        elif isinstance(myctx, commands.Context):
            author = myctx.author
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
                    Muted by: {author.mention} ({author.id})
                    """
                ).add_field(
                    name="**Reason:**",
                    value=f"{reason}"
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
                Muted by: {author.mention} ({author.id})
                """
            ).add_field(
                name="**Reason:**",
                value=f"{reason}"
            )
        )

    @commands.command(name="timeout", aliases=["mute"])
    async def timeout(self, ctx, member: nextcord.Member, time: str = "900", *, reason):
        await self.shh(ctx, member, time, reason)

    @nextcord.slash_command()
    async def my_select_command(self,
        interaction: Interaction,
        member: nextcord.Member = SlashOption(name="member", description="which member to be muted?", required=True),
        time: str = SlashOption(name="time", description="For how long should the user be muted?", required=False, default=900),
        reason: str = SlashOption(name="reason", description="Why is the user muted?", required=False, default="No reason given.")
    ):
        await self.shh(interaction, member, time, reason)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, nextcord.Forbidden):
            return await ctx.send("Forbidden sad.")
        elif isinstance(error, nextcord.HTTPException):
            return await ctx.send("Weird error, try again.")

def setup(bot):
    bot.add_cog(Mute(bot))