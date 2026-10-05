import discord
from discord.ext import commands
from discord import app_commands

class ModVCDeafen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vcdeafen", description="設置功能")
    @app_commands.describe(member="Parameter description", deafen="True  / False ")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_vcdeafen(self, interaction: discord.Interaction, member: discord.Member, deafen: bool):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ Channel", ephemeral=True)
            return
        
        try:
            await member.edit(deafen=deafen, reason=f" {interaction.user} Settings")
            action = "[HEADPHONES] Server" if deafen else " Server"
            await interaction.response.send_message(f"✅ {action}{member.mention}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ SettingsFailed{e}", ephemeral=True)

    @mod_vcdeafen.error
    async def mod_vcdeafen_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCDeafen(bot))
