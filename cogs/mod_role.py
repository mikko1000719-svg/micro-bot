import discord
from discord.ext import commands
from discord import app_commands

class ModRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. 賦予身分組指令
    @app_commands.command(name="role_add", description="為指定的成員新增一個身分組")
    @app_commands.describe(member="要新增身分組的成員", role="要賦予的身分組")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_add(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        # 檢查機器人自身的權限與身分組階級
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message("❌ 失敗：該身分組的階級高於或等於我的最高身分組，我無法指派它！", ephemeral=True)
            return

        try:
            await member.add_roles(role, reason=f"由管理員 {interaction.user} 透過指令賦予")
            await interaction.response.send_message(f"✅ 成功將身分組 {role.mention} 賦予給 {member.mention}！")
        except Exception as e:
            await interaction.response.send_message(f"❌ 賦予身分組失敗：{e}", ephemeral=True)

    @role_add.error
    async def role_add_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「管理身分組」的權限！", ephemeral=True)

    # 2. 移除身分組指令
    @app_commands.command(name="role_remove", description="從指定的成員身上移除一個身分組")
    @app_commands.describe(member="要移除身分組的成員", role="要移除的身分組")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_remove(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message("❌ 失敗：該身分組的階級高於或等於我的最高身分組，我無法移除它！", ephemeral=True)
            return

        try:
            await member.remove_roles(role, reason=f"由管理員 {interaction.user} 透過指令移除")
            await interaction.response.send_message(f"✅ 成功從 {member.mention} 身上移除身分組 {role.mention}！")
        except Exception as e:
            await interaction.response.send_message(f"❌ 移除身分組失敗：{e}", ephemeral=True)

    @role_remove.error
    async def role_remove_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「管理身分組」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModRole(bot))