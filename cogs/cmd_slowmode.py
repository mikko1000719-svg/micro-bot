import discord
from discord.ext import commands
from discord import app_commands

class CmdSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slowmode", description="設置")
    @app_commands.describe(seconds=" ( 0  21600 )")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        if seconds < 0 or seconds > 21600:
            await interaction.response.send_message("❌  0  21600 ", ephemeral=True)
            return
            
        await interaction.channel.edit(slowmode_delay=seconds, reason=f"Manage {interaction.user} ")
        
        if seconds == 0:
            embed = discord.Embed(title="⏱ ", description="頻道", color=discord.Color.green())
        else:
            embed = discord.Embed(title="⏱ Start", description=f"Settings **{seconds} **", color=discord.Color.orange())
            
        await interaction.response.send_message(embed=embed)

    @slowmode.error
    async def slowmode_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManageChannelPermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdSlowmode(bot))