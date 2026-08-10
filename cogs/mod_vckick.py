import discord
from discord.ext import commands
from discord import app_commands

class ModVCKick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vckick", description="將指定成員從語音頻道中踢出")
    @app_commands.describe(member="要踢出語音的成員")
    @app_commands.checks.has_permissions(move_members=True)
    async def mod_vckick(self, interaction: discord.Interaction, member: discord.Member):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ 該成員目前不在任何語音頻道中！", ephemeral=True)
            return

        try:
            # 將成員移動到 None 頻道，即可將其踢出語音
            await member.move_to(None, reason=f"由 {interaction.user} 踢出語音")
            await interaction.response.send_message(f"🚪 成功將 {member.mention} 踢出語音頻道！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 踢出語音失敗：{e}", ephemeral=True)

    @mod_vckick.error
    async def mod_vckick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「移動成員」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCKick(bot))