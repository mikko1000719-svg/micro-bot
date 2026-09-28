import discord
from discord.ext import commands
from discord import app_commands

class ModSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_slowmode", description="設置")
    @app_commands.describe(seconds=" ( 0  21600 )")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_slowmode(self, interaction: discord.Interaction, seconds: int):
        if seconds < 0 or seconds > 21600:
            await interaction.response.send_message("❌  0  21600 ", ephemeral=True)
            return

        try:
            await interaction.channel.edit(slowmode_delay=seconds, reason=f" {interaction.user} Settings")
            if seconds == 0:
                await interaction.response.send_message("⏱ Channel")
            else:
                await interaction.response.send_message(f"⏱ Channel **{seconds}** ")
        except Exception as e:
            await interaction.response.send_message(f"❌ SettingsFailed{e}", ephemeral=True)

    @mod_slowmode.error
    async def mod_slowmode_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModSlowmode(bot))
