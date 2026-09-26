import discord
from discord.ext import commands
from discord import app_commands

class ModVCMute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vcmute", description="SettingsServer")
    @app_commands.describe(member="", mute="True  / False ")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_vcmute(self, interaction: discord.Interaction, member: discord.Member, mute: bool):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("[ERROR] ChannelPermissionUpdate", ephemeral=True)
        
        try:
            await member.edit(mute=mute, reason=f" {interaction.user} Settings")
            action = " Server" if mute else " Server"
            await interaction.response.send_message(f"[OK] Success {member.mention}  **{action}**", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] SettingsFailed{e}", ephemeral=True)

    @mod_vcmute.error
    async def mod_vcmute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCMute(bot))
