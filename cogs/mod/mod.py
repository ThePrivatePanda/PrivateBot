import nextcord, datetime
from nextcord.ext import commands
from nextcord.errors import Forbidden, HTTPException

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def bon(self, stuff, user: nextcord.User, *, reason="No reason."):
        myctx = self.bot.WrapStuff(stuff)
        if user.id == self.bot.user.id:
            return await myctx.send("Simply: No.")

        if user.id == myctx.author.id:
            return await myctx.send("Ask someone higher than you to ban you.")

        if user in myctx.guild.members:
            if myctx.author.top_role <= user.top_role:
                return await myctx.send("You are not high enough in the role hierarchy to ban them.")

        try:
            await myctx.guild.ban(user, reason=f"{myctx.author.name} ({myctx.author.id}) banned {user.name} ({user.id}) for: {reason}")
        except Forbidden:
            return await myctx.send("You are not allowed to ban them!")
        except HTTPException:
            return await myctx.send("Some error occured, try again.")

        em=nextcord.Embed(
            title="You were banned!",
            description=f"You were banned from `{myctx.guild.name}` ({myctx.guild.id}) for reason:\n{reason}\nAppeals server link: {self.bot.appeal_server_invite}",
            colour = nextcord.Colour.red())
        em.set_footer(
            icon_url=myctx.guild.icon.url)
        em.timestamp = nextcord.utils.utcnow()

        user_dm = await self.bot.get_user_dm()
        if user_dm:
            await user.send(embed=em)
        return await myctx.send(embed=nextcord.Embed(title="Success!", description=f"Banned `{user.name}` ({user.id}) for: {reason}", colour=nextcord.colour.green()))

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: nextcord.User, *, reason="No reason."):
        await self.bon(ctx, user, reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, user: nextcord.user, delete_days: int = 3):

        if user in ctx.guild.members:
            if ctx.author.top_role <= user.top_role:
                return await ctx.send(embed=nextcord.Embed(title="Error!", description="They are too high in the role hierarchy for you to ban them.", colour=nextcord.colour.red))

        try:
            await ctx.guild.ban(user, reason=f"{ctx.author.name} ({ctx.author.id}) banned {user.name} ({user.id}) to clear the last {delete_days} days messages of the user.", delete_days=delete_days)
            await ctx.guild.unban(user, reason="Softban over.")
        except Forbidden:
            return await ctx.send(embed=nextcord.Embed(title="Error!", description="You are not allowed to ban them!", colour=nextcord.colour.red))
        except HTTPException:
            return await ctx.send(embed=nextcord.Embed(title="Error!", description="Some error occured, try again.", colour=nextcord.colour.red))

        em=nextcord.Embed(
            title="You were banned (and unbanned)!",
            description=f"You were banned from `{ctx.guild.name}` ({ctx.guild.id}) to clear the last {delete_days} days messages from you. \nsUse this link to join back: {self.bot.main_server_invite}",
            colour = nextcord.Colour.blue()).set_footer(
                icon_url=ctx.guild.icon_url)
        em.timestamp = nextcord.utils.utcnow()

        await ctx.send(embed=em)
        return await ctx.send(embed=nextcord.Embed(title="Success!", description=f"SoftBanned `{user.name}` ({user.id}) to clear the last {delete_days} days messages of the user.\n**User has been unbanned.**", colour=nextcord.colour.green))

    @commands.command(name="timeout", aliases=["mute"])
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout(ctx, member: nextcord.Member, time: int = 900):
        datetime_instance = nextcord.utils.utcnow() + nextcord.utils.timedelta(seconds=time)
        muted_till = nextcord.utils.format_dt(datetime_instance, "F")
        await member.edit(timeout=muted_till)
        await member.send(f'You have been muted in `` for ``. Automatic Unmute on .')
        await ctx.channel.send(f"`` has been muted for ``, Automatic Unmute on ")

    @commands.command(name="untimeout", aliases=["unmute","un-mute", "un-timeout"])
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def un_timeout(ctx, member: nextcord.Member):
        await member.edit(timeout=None)
        await member.send(f'You have been unmuted in `` for ``. Automatic Unmute on .')
        await ctx.channel.send(f"`` has been muted for ``, Automatic Unmute on ")

def setup(bot):
    bot.add_cog(Moderation(bot))