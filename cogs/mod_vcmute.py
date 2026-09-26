import discord
from discord.ext import commands
from discord import app_commands

class ModVCMute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vcmute", description="Settings成員的Server語音靜音狀態")
    @app_commands.describe(member="目標成員", mute="True 靜音 / False 解除靜音")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_vcmute(self, interaction: discord.Interaction, member: discord.Member, mute: bool):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("[ERROR] 該成員目前不在任何語音Channel中，但Permission仍會Update。", ephemeral=True)
        
        try:
            await member.edit(mute=mute, reason=f"由 {interaction.user} Settings語音靜音")
            action = "🔇 Server靜音" if mute else "🔊 解除Server靜音"
            await interaction.response.send_message(f"[OK] 已Success將 {member.mention} 設為 **{action}**！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] Settings語音靜音Failed：{e}", ephemeral=True)

    @mod_vcmute.error
    async def mod_vcmute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCMute(bot))
