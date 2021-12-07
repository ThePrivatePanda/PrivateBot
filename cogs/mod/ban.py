import discord, datetime
from discord.ext import commands
from discord.errors import Forbidden, HTTPException

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason=None):
        if user.id == self.bot.user.id:
            return await ctx.send("Simply: No.")

        if user.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Error!", description="Ask someone higher than you to ban you.", colour=discord.colour.red()))

        if user in ctx.guild.members:
            if ctx.author.top_role < user.top_role or ctx.author.top_role == user.top_role:
                return await ctx.send(embed=discord.Embed(title="Error!", description="You are not high enough in the role hierarchy to ban them.", colour=discord.colour.red()))

        if reason is None:
            reason = "No reason specified."

        try:
            await ctx.guild.ban(user, reason=f"{ctx.author.name} ({ctx.author.id}) banned {user.name} ({user.id}) for: {reason}")
        except Forbidden:
            return await ctx.send(embed=discord.Embed(title="Error!", description="You are not allowed to ban them!", colour=discord.colour.red()))
        except HTTPException:
            return await ctx.send(embed=discord.Embed(title="Error!", description="Some error occured, try again.", colour=discord.colour.red()))

        em=discord.Embed(
            title="You were banned!",
            description=f"You were banned from `{ctx.guild.name}` ({ctx.guild.id}) for reason:\n{reason}\nAppeals server link: {self.bot.appeal_link}",
            colour = discord.Colour.red())
        em.set_footer(
            icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()

        await self.bot.get_user_dm().send(embed=em)
        return await ctx.send(embed=discord.Embed(title="Success!", description=f"Banned `{user.name}` ({user.id}) for: {reason}", colour=discord.colour.green()))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.user, delete_days=None):

        if delete_days is None:
            delete_days = 3

        if user in ctx.guild.members:
            if ctx.author.top_role < user.top_role or ctx.author.top_role == user.top_role:
                return await ctx.send(embed=discord.Embed(title="Error!", description="They are too high in the role hierarchy for you to ban them.", colour=discord.colour.red))

        try:
            await ctx.guild.ban(user, reason=f"{ctx.author.name} ({ctx.author.id}) banned {user.name} ({user.id}) to clear the last {delete_days} days messages of the user", delete_days=delete_days)
            await ctx.guild.unban(user, "Softban over.")
        except Forbidden:
            return await ctx.send(embed=discord.Embed(title="Error!", description="You are not allowed to ban them!", colour=discord.colour.red))
        except HTTPException:
            return await ctx.send(embed=discord.Embed(title="Error!", description="Some error occured, try again.", colour=discord.colour.red))

        em=discord.Embed(
            title="You were banned!",
            description=f"You were banned from `{ctx.guild.name}` ({ctx.guild.id}) to clear the last {delete_days} days messages from you. \nsUse this link to join back <SERVER INVITE LINK>",
            colour = discord.Colour.blue())
        em.set_footer(
            icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        
        await ctx.send(embed=em)
        return await ctx.send(embed=discord.Embed(title="Success!", description=f"SoftBanned `{user.name}` ({user.id}) to clear the last {delete_days} days messages of the user.\n**User has been unbanned.**", colour=discord.colour.green))

def setup(bot):
    bot.add_cog(Moderation(bot))