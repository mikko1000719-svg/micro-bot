import discord
from discord.ext import commands
from discord import app_commands

class ModSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_slowmode", description="Settings目前Channel的緩慢模式 (冷卻時間)")
    @app_commands.describe(seconds="冷卻秒數 (輸入 0 則關閉緩慢模式，最高 21600 秒)")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_slowmode(self, interaction: discord.Interaction, seconds: int):
        if seconds < 0 or seconds > 21600:
            await interaction.response.send_message("[ERROR] 秒數必須介於 0 到 21600 秒之間！", ephemeral=True)
            return

        try:
            await interaction.channel.edit(slowmode_delay=seconds, reason=f"由 {interaction.user} Settings緩慢模式")
            if seconds == 0:
                await interaction.response.send_message("⏱️ 已經關閉本Channel的緩慢模式。")
            else:
                await interaction.response.send_message(f"⏱️ 已經將本Channel的緩慢模式設為每人發言需等待 **{seconds}** 秒。")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] Settings緩慢模式Failed：{e}", ephemeral=True)

    @mod_slowmode.error
    async def mod_slowmode_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModSlowmode(bot))
