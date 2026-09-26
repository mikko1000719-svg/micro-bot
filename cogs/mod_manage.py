import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class ModManage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mute", description="將指定成員禁言一段時間")
    @app_commands.describe(member="要禁言的成員", minutes="禁言的分鐘數", reason="禁言的原因")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "無提供原因"):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("[ERROR] 你無法禁言階級比你高或同階級的成員。", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            embed = discord.Embed(
                title="🔇 禁言成功",
                description=f"已成功禁言 {member.mention} **{minutes} 分鐘**。\n原因：`{reason}`",
                color=discord.Color.orange()
            )
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"[ERROR] 執行失敗：{e}", ephemeral=True)

    @app_commands.command(name="unmute", description="解除指定成員的禁言")
    @app_commands.describe(member="要解除禁言的成員")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        try:
            await member.timeout(None, reason="解除禁言")
            embed = discord.Embed(
                title="🔊 已解除禁言",
                description=f"已成功解除 {member.mention} 的禁言限制。",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 執行失敗：{e}", ephemeral=True)

    # 綁定錯誤處理
    @mute.error
    @unmute.error
    async def mod_manage_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「管理員」權限才能使用此指令！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModManage(bot))
