import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
import discord.abc

class Punchclock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Staff")
    @commands.command(aliases=["ci"])
    async def clockin(ctx):
        """Allows a user with the required staff role to mark themself as available."""
        global clocklist
        if ctx.author not in clocklist:
            clocklist.append(ctx.author)
            e = discord.Embed(colour=discord.Colour(0x57F287), description="You've clocked in successfully!")
            await ctx.send(embed=e)
        else:
            e = discord.Embed(colour=discord.Colour(0xFEE75C), description="You're already clocked in!")
            await ctx.send(embed=e)

    @commands.has_role("Staff")
    @commands.command(aliases=["co"])
    async def clockout(ctx):
        """Allows a user with the required staff role to mark themself as unavailable."""
        global clocklist
        if ctx.author not in clocklist:
            e = discord.Embed(colour=discord.Colour(0xFEE75C), description="You're not clocked in!")
            await ctx.send(embed=e)
        else:
            clocklist.remove(ctx.author)
            e = discord.Embed(colour=discord.Colour(0x57F287), description="You're clocked out!")
            await ctx.send(embed=e)

    @commands.command(aliases=["staff"])
    async def seestaff(ctx):
        """Allows any user to query the list of staff who have marked themselves available."""
        if not clocklist:
            e = discord.Embed(colour=discord.Colour(0xFEE75C), description="Unfortunately, there are no staff available at this time.")
            await ctx.send(embed=e)
        else:
            onlinelist = []
            for x in clocklist:
                onlinelist.append(x.name)
            embed=discord.Embed(title="Please gauge staff availability by this list and not user statuses.", description=str(onlinelist).strip("[]")+"\n")
            embed.set_author(name="Punchclock", url="https://github.com/royalPanic/punchclock")
            embed.set_footer(text="Powered by Punchclock")
            await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Punchclock(bot))
