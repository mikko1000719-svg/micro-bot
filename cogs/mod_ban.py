import discord
from discord.ext import commands
from discord import app_commands

class ModBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="封禁用戶")
    @app_commands.describe(member="要封禁的成員", reason="封禁原因")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = ""):
        if member == interaction.user:
            await interaction.response.send_message("❌ 你不能封禁自己", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"✅ 已封禁 {member.mention}\n原因: {reason}")
        except Exception as e:
            await interaction.response.send_message(f"❌ 封禁失敗: {e}", ephemeral=True)

    @mod_ban.error
    async def mod_ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModBan(bot))
