import discord
from discord.ext import commands
from discord import app_commands

class ModRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="role_add", description="為指定的成員新增一個身分組")
    @app_commands.describe(member="要新增身分組的成員", role="要賦予的身分組")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def role_add(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message("[ERROR] Failed：該身分組的階級高於或等於我的最高身分組，我無法指派它！", ephemeral=True)
            return

        try:
            await member.add_roles(role, reason=f"由Manage員 {interaction.user} 透過Command賦予")
            await interaction.response.send_message(f"[OK] Success將身分組 {role.mention} 賦予給 {member.mention}！")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 賦予身分組Failed：{e}", ephemeral=True)

    @app_commands.command(name="role_remove", description="從指定的成員身上移除一個身分組")
    @app_commands.describe(member="要移除身分組的成員", role="要移除的身分組")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def role_remove(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message("[ERROR] Failed：該身分組的階級高於或等於我的最高身分組，我無法移除它！", ephemeral=True)
            return

        try:
            await member.remove_roles(role, reason=f"由Manage員 {interaction.user} 透過Command移除")
            await interaction.response.send_message(f"[OK] Success從 {member.mention} 身上移除身分組 {role.mention}！")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 移除身分組Failed：{e}", ephemeral=True)

    @role_add.error
    @role_remove.error
    async def mod_role_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModRole(bot))
