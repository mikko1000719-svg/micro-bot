import discord
from discord.ext import commands
from discord import app_commands

class ModUnlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_unlock", description="解鎖目前頻道，恢復一般成員發言權限")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def mod_unlock(self, interaction: discord.Interaction):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None  # 恢復預設
        
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason=f"由 {interaction.user} 解鎖頻道")
            await interaction.response.send_message("🔓 此頻道已解鎖，恢復正常發言。")
        except Exception as e:
            await interaction.response.send_message(f"❌ 解鎖頻道失敗：{e}", ephemeral=True)

    @mod_unlock.error
    async def mod_unlock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「管理頻道」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModUnlock(bot))