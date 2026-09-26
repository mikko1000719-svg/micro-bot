import discord
from discord.ext import commands
from discord import app_commands

class ModVCMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vcmove", description="將成員從目前語音頻道移動至另一個語音頻道")
    @app_commands.describe(member="要移動的成員", target_channel="目標語音頻道")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_vcmove(self, interaction: discord.Interaction, member: discord.Member, target_channel: discord.VoiceChannel):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("[ERROR] 該成員目前不在任何語音頻道中！", ephemeral=True)
            return

        try:
            old_channel = member.voice.channel
            await member.move_to(target_channel, reason=f"由 {interaction.user} 移動")
            await interaction.response.send_message(
                f"🚚 成功將 {member.mention} 從 **{old_channel.name}** 移動至 **{target_channel.name}**！",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 移動成員失敗：{e}", ephemeral=True)

    @mod_vcmove.error
    async def mod_vcmove_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「管理員」權限才能使用此指令！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCMove(bot))
