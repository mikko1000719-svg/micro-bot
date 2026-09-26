import discord
from discord.ext import commands
from discord import app_commands

class ModServerUnlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_server_unlock", description="【解除】解鎖伺服器內所有文字頻道")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_server_unlock(self, interaction: discord.Interaction):
        await interaction.response.send_message("[UNLOCK] **全伺服器解鎖程序啟動中...**", ephemeral=True)
        
        unlocked_count = 0
        for channel in interaction.guild.text_channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            if overwrite.send_messages is False:
                overwrite.send_messages = None
                try:
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason="管理員解除全伺服器鎖定")
                    unlocked_count += 1
                except discord.Forbidden:
                    continue

        await interaction.followup.send(f"[OK] 全伺服器解鎖完成！已解鎖 **{unlocked_count}** 個文字頻道。")

    @mod_server_unlock.error
    async def mod_server_unlock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「管理員」權限才能解鎖全伺服器！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModServerUnlock(bot))
