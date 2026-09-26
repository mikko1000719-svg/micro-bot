import discord
from discord.ext import commands
from discord import app_commands

class ModNick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_nick", description="更改指定成員在伺服器中的顯示暱稱")
    @app_commands.describe(member="要改暱稱的成員", nickname="新的暱稱 (留空則清除自訂暱稱)")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_nick(self, interaction: discord.Interaction, member: discord.Member, nickname: str = None):
        try:
            await member.edit(nick=nickname, reason=f"由 {interaction.user} 透過指令更改")
            if nickname:
                await interaction.response.send_message(f"✏️ 成功將 {member.mention} 的暱稱改為 **{nickname}**！")
            else:
                await interaction.response.send_message(f"[SWITCH] 成功將 {member.mention} 的暱稱重置回原名稱！")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 更改暱稱失敗（可能該成員身分組高於機器人）：{e}", ephemeral=True)

    @mod_nick.error
    async def mod_nick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「管理員」權限才能使用此指令！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModNick(bot))
