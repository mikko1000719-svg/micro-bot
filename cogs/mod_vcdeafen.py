import discord
from discord.ext import commands
from discord import app_commands

class ModVCDeafen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vcdeafen", description="Settings成員的Server拒聽狀態 (聽不到別人聲音)")
    @app_commands.describe(member="目標成員", deafen="True 拒聽 / False 解除拒聽")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_vcdeafen(self, interaction: discord.Interaction, member: discord.Member, deafen: bool):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("[ERROR] 該成員目前不在任何語音Channel中，無法套用拒聽。", ephemeral=True)
            return
        
        try:
            await member.edit(deafen=deafen, reason=f"由 {interaction.user} Settings語音拒聽")
            action = "[HEADPHONES] 已設為Server拒聽" if deafen else "🔊 已解除Server拒聽"
            await interaction.response.send_message(f"[OK] {action}：{member.mention}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] SettingsFailed：{e}", ephemeral=True)

    @mod_vcdeafen.error
    async def mod_vcdeafen_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCDeafen(bot))
