import discord
from discord.ext import commands
from discord import app_commands

class ModVCKick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vckick", description="頻道")
    @app_commands.describe(member="Parameter description")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_vckick(self, interaction: discord.Interaction, member: discord.Member):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ Channel", ephemeral=True)
            return

        try:
            await member.move_to(None, reason=f" {interaction.user} ")
            await interaction.response.send_message(f" Success {member.mention} Channel", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed{e}", ephemeral=True)

    @mod_vckick.error
    async def mod_vckick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCKick(bot))
