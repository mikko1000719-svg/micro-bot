import discord
from discord.ext import commands
from discord import app_commands

class ModVCMute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vcmute", description="設定成員的伺服器語音靜音狀態")
    @app_commands.describe(member="目標成員", mute="True 靜音 / False 解除靜音")
    @app_commands.checks.has_permissions(mute_members=True)
    async def mod_vcmute(self, interaction: discord.Interaction, member: discord.Member, mute: bool):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ 該成員目前不在任何語音頻道中，但權限仍會更新。", ephemeral=True)
            # 即使不在語音中，也能編輯該成員的靜音屬性
        
        try:
            await member.edit(mute=mute, reason=f"由 {interaction.user} 設定語音靜音")
            action = "🔇 伺服器靜音" if mute else "🔊 解除伺服器靜音"
            await interaction.response.send_message(f"✅ 已成功將 {member.mention} 設為 **{action}**！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 設定語音靜音失敗：{e}", ephemeral=True)

    @mod_vcmute.error
    async def mod_vcmute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「靜音成員」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCMute(bot))