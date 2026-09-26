import discord
from discord.ext import commands
from discord import app_commands

class ModUnban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_unban", description="透過使用者 ID 解除成員的封鎖狀態")
    @app_commands.describe(user_id="要解除封鎖的使用者 ID (純Number)", reason="解封原因 (選填)")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_unban(self, interaction: discord.Interaction, user_id: str, reason: str = "Manage員解封"):
        try:
            user_obj = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user_obj, reason=reason)
            await interaction.response.send_message(f"[OK] 已經Success解除使用者 `{user_obj.name}` 的封鎖！")
        except ValueError:
            await interaction.response.send_message("[ERROR] 請輸入有效的Number User ID！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 解除封鎖Failed（找不到該User或未被封鎖）：{e}", ephemeral=True)

    @mod_unban.error
    async def mod_unban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModUnban(bot))
