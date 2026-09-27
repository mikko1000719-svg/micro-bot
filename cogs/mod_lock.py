import discord
from discord.ext import commands
from discord import app_commands

class ModLock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_lock", description="Channel")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_lock(self, interaction: discord.Interaction):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason=f" {interaction.user} Channel")
            await interaction.response.send_message("🔒 ChannelSuccessTemporary")
        except Exception as e:
            await interaction.response.send_message(f"❌ ChannelFailed{e}", ephemeral=True)

    @mod_lock.error
    async def mod_lock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModLock(bot))
