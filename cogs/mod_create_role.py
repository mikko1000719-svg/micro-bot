import discord
from discord.ext import commands
from discord import app_commands

class ModCreateRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_create_role", description="在伺服器中建立一個新的身分組")
    @app_commands.describe(name="身分組名稱")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mod_create_role(self, interaction: discord.Interaction, name: str):
        try:
            guild = interaction.guild
            new_role = await guild.create_role(name=name, reason=f"由 {interaction.user} 建立")
            await interaction.response.send_message(f"🏷️ 成功建立身分組 {new_role.mention}！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 建立身分組失敗：{e}", ephemeral=True)

    @mod_create_role.error
    async def mod_create_role_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「管理身分組」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModCreateRole(bot))