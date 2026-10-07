import discord
from discord.ext import commands
from discord import app_commands

class ModVCKick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="vckick", description="將用戶踢出語音頻道")
    @app_commands.describe(member="要踢出的成員")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_vckick(self, interaction: discord.Interaction, member: discord.Member):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ 該成員不在語音頻道中", ephemeral=True)
            return

        try:
            await member.move_to(None, reason=f"被 {interaction.user} 踢出")
            await interaction.response.send_message(f"✅ 已將 {member.mention} 踢出語音頻道", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 踕出失敗: {e}", ephemeral=True)

    @mod_vckick.error
    async def mod_vckick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCKick(bot))
