import discord
from discord.ext import commands
from discord import app_commands

class ModNick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_nick", description="更改指定成員在Server中的Display暱稱")
    @app_commands.describe(member="要改暱稱的成員", nickname="新的暱稱 (留空則清除Custom暱稱)")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_nick(self, interaction: discord.Interaction, member: discord.Member, nickname: str = None):
        try:
            await member.edit(nick=nickname, reason=f"由 {interaction.user} 透過Command更改")
            if nickname:
                await interaction.response.send_message(f"✏️ Success將 {member.mention} 的暱稱改為 **{nickname}**！")
            else:
                await interaction.response.send_message(f"[SWITCH] Success將 {member.mention} 的暱稱重置回原名稱！")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 更改暱稱Failed（可能該成員身分組高於Bot）：{e}", ephemeral=True)

    @mod_nick.error
    async def mod_nick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModNick(bot))
