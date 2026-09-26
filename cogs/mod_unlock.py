import discord
from discord.ext import commands
from discord import app_commands

class ModUnlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_unlock", description="Channel，Permission")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_unlock(self, interaction: discord.Interaction):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None  
        
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason=f" {interaction.user} Channel")
            await interaction.response.send_message("[UNLOCK] Channel，。")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] ChannelFailed：{e}", ephemeral=True)

    @mod_unlock.error
    async def mod_unlock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 「Manage」PermissionCommand！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModUnlock(bot))
