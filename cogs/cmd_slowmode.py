import discord
from discord.ext import commands
from discord import app_commands

class CmdSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slowmode", description="設定當前頻道的慢速模式冷卻時間")
    @app_commands.describe(seconds="冷卻秒數 (輸入 0 即為關閉，最大 21600 秒)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        if seconds < 0 or seconds > 21600:
            await interaction.response.send_message("❌ 秒數必須介於 0 到 21600 秒之間！", ephemeral=True)
            return
            
        await interaction.channel.edit(slowmode_delay=seconds, reason=f"由管理員 {interaction.user} 調整慢速模式")
        
        if seconds == 0:
            embed = discord.Embed(title="⏱️ 慢速模式已關閉", description="本頻道已解除發言冷卻限制。", color=discord.Color.green())
        else:
            embed = discord.Embed(title="⏱️ 慢速模式已啟動", description=f"發言冷卻時間已設定為 **{seconds} 秒**。", color=discord.Color.orange())
            
        await interaction.response.send_message(embed=embed)

    @slowmode.error
    async def slowmode_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你需要「管理頻道」權限才能使用此指令！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdSlowmode(bot))