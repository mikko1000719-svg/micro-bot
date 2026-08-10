import discord
from discord.ext import commands
from discord import app_commands

class ModUnban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_unban", description="透過使用者 ID 解除成員的封鎖狀態")
    @app_commands.describe(user_id="要解除封鎖的使用者 ID (純數字)", reason="解封原因 (選填)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def mod_unban(self, interaction: discord.Interaction, user_id: str, reason: str = "管理員解封"):
        try:
            user_obj = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user_obj, reason=reason)
            await interaction.response.send_message(f"✅ 已經成功解除使用者 `{user_obj.name}` 的封鎖！")
        except ValueError:
            await interaction.response.send_message("❌ 請輸入有效的數字 User ID！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 解除封鎖失敗（找不到該用戶或未被封鎖）：{e}", ephemeral=True)

    @mod_unban.error
    async def mod_unban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「封鎖成員」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModUnban(bot))