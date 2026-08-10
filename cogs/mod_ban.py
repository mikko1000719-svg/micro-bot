import discord
from discord.ext import commands
from discord import app_commands

class ModBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_ban", description="將指定的成員永久封鎖 (Ban)")
    @app_commands.describe(member="要封鎖的成員", reason="封鎖原因 (選填)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def mod_ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "無原因"):
        if member == interaction.user:
            await interaction.response.send_message("你不能把自己封鎖！", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"🔨 已經將 {member.mention} 成功封鎖。\n原因：{reason}")
        except Exception as e:
            await interaction.response.send_message(f"❌ 封鎖失敗：{e}", ephemeral=True)

    @mod_ban.error
    async def mod_ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「封鎖成員」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModBan(bot))