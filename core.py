# Import Stack
import discord
from discord_slash import SlashCommand
from discord.ext import commands
import jthon
from pathlib import Path
import os
from discord.ext.commands import has_permissions
from discord.utils import get
import discord.abc

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color(0x57F287), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

# Variable Defs
help_command = commands.DefaultHelpCommand(no_category = 'Other Commands')
config = jthon.load('config')
token = str(config.get("token")) #pulls the bot token from the hidden config file
bot = commands.Bot(
    command_prefix = commands.when_mentioned_or('^'),
    description = "A simple bot designed to help users see when staff are available.",
    help_command = None
)
bot.help_command = MyHelpCommand()
clocklist = []
slash = SlashCommand(bot, sync_commands=True)

# Function Defs
def automatic_cog_load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

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

automatic_cog_load()

bot.run(token)