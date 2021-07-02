import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandPermissionType
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
import discord.abc

class Slashclock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    slash = SlashCommand(bot, sync_commands=True)

    @slash.slash(name="test", description="This is just a test command, nothing more.")
    @slash.permission(guild_id=800289611934597130, permissions=[create_permission(848473542143770634, SlashCommandPermissionType.ROLE, True), create_permission(800289611934597130, SlashCommandPermissionType.ROLE, False)])
    async def test(ctx):
        await ctx.send(content="Hello World!")

def setup(bot):
	bot.add_cog(Punchclock(bot))