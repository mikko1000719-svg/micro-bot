import discord
from discord.ext import commands
from discord import app_commands

class ModVCDeafen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vcdeafen", description="設定成員的伺服器拒聽狀態 (聽不到別人聲音)")
    @app_commands.describe(member="目標成員", deafen="True 拒聽 / False 解除拒聽")
    @app_commands.checks.has_permissions(deafen_members=True)
    async def mod_vcdeafen(self, interaction: discord.Interaction, member: discord.Member, deafen: bool):
        # 檢查該成員是否在語音頻道中
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ 該成員目前不在任何語音頻道中，無法套用拒聽。", ephemeral=True)
            return
        
        try:
            # 編輯成員的 deafen 屬性
            await member.edit(deafen=deafen, reason=f"由 {interaction.user} 設定語音拒聽")
            action = "🎧 已設為伺服器拒聽" if deafen else "🔊 已解除伺服器拒聽"
            await interaction.response.send_message(f"✅ {action}：{member.mention}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 設定失敗：{e}", ephemeral=True)

    @mod_vcdeafen.error
    async def mod_vcdeafen_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「拒聽成員」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCDeafen(bot))