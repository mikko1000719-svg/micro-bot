import discord
from discord.ext import commands
from discord import app_commands

class ModServerLock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_server_lock", description="【緊急】鎖定伺服器內所有文字頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_server_lock(self, interaction: discord.Interaction):
        await interaction.response.send_message("🚨 **全伺服器鎖定程序啟動中...**", ephemeral=True)
        
        locked_count = 0
        # 迴圈讀取伺服器內所有的文字頻道
        for channel in interaction.guild.text_channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            # 如果尚未被鎖定，則關閉發言權限
            if overwrite.send_messages is not False:
                overwrite.send_messages = False
                try:
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason="管理員啟動全伺服器鎖定")
                    locked_count += 1
                except discord.Forbidden:
                    continue # 若機器人權限不足則跳過該頻道

        await interaction.followup.send(f"🔒 全伺服器鎖定完成！已鎖定 **{locked_count}** 個文字頻道。")

    @mod_server_lock.error
    async def mod_server_lock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 此為高危險指令，你需要「管理員」權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModServerLock(bot))