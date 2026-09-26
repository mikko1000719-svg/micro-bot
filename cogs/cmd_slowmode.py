import discord
from discord.ext import commands
from discord import app_commands

class CmdSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slowmode", description="Settings當前Channel的慢速模式冷卻時間")
    @app_commands.describe(seconds="冷卻秒數 (輸入 0 即為關閉，最大 21600 秒)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        if seconds < 0 or seconds > 21600:
            await interaction.response.send_message("[ERROR] 秒數必須介於 0 到 21600 秒之間！", ephemeral=True)
            return
            
        await interaction.channel.edit(slowmode_delay=seconds, reason=f"由Manage員 {interaction.user} 調整慢速模式")
        
        if seconds == 0:
            embed = discord.Embed(title="⏱️ 慢速模式已關閉", description="本Channel已解除發言冷卻Limit。", color=discord.Color.green())
        else:
            embed = discord.Embed(title="⏱️ 慢速模式已Start", description=f"發言冷卻時間已Settings為 **{seconds} 秒**。", color=discord.Color.orange())
            
        await interaction.response.send_message(embed=embed)

    @slowmode.error
    async def slowmode_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「ManageChannel」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdSlowmode(bot))