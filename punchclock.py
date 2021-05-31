# Import Stack
import discord
from discord.ext import commands
import jthon
from pathlib import Path
import os
from discord.ext.commands import has_permissions
from discord.utils import get
import discord.abc

# Variable Defs
help_command = commands.DefaultHelpCommand(no_category = 'Commands')
config = jthon.load('config')
token = str(config.get("token")) #pulls the bot token from the hidden config file
bot = commands.Bot(
    command_prefix = commands.when_mentioned_or('^'),
    description = "A simple bot designed to help users see when staff are available.",
    help_command = help_command
)
clocklist = []

#Bot Events
@bot.event
async def on_ready():
    print("Punchclock is operational!")

@bot.event 
async def on_command_error(ctx, error):
    e = discord.Embed(colour=discord.Colour(0xED4245), description=f"{error}")
    await ctx.send(embed=e)

#Bot Commands
@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    """Allows the owner of the bot to shut down the bot from within Discord."""
    e = discord.Embed(colour=discord.Colour(0x57F287), description="Command Received, Shutting down Punchclock!")
    await ctx.send(embed=e)
    exit()

@commands.has_role("Staff")
@bot.command(aliases=["ci"])
async def clockin(ctx):
    global clocklist
    if ctx.author not in clocklist:
        clocklist.append(ctx.author)
        e = discord.Embed(colour=discord.Colour(0x57F287), description="You've clocked in successfully!")
        await ctx.send(embed=e)
    else:
        e = discord.Embed(colour=discord.Colour(0xFEE75C), description="You're already clocked in!")
        await ctx.send(embed=e)

@commands.has_role("Staff")
@bot.command(aliases=["co"])
async def clockout(ctx):
    global clocklist
    if ctx.author not in clocklist:
        e = discord.Embed(colour=discord.Colour(0xFEE75C), description="You're not clocked in!")
        await ctx.send(embed=e)
    else:
        clocklist.remove(ctx.author)
        e = discord.Embed(colour=discord.Colour(0x57F287), description="You're clocked out!")
        await ctx.send(embed=e)

@bot.command(aliases=["staff"])
async def seestaff(ctx):
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

bot.run(token)