import discord
from discord.ext import commands
from discord import app_commands

class ModServerLock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_server_lock", description="伺服器")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_server_lock(self, interaction: discord.Interaction):
        await interaction.response.send_message(" **ServerStart...**", ephemeral=True)
        
        locked_count = 0
        for channel in interaction.guild.text_channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            if overwrite.send_messages is not False:
                overwrite.send_messages = False
                try:
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason="ManageStartServer")
                    locked_count += 1
                except discord.Forbidden:
                    continue 

        await interaction.followup.send(f"🔒 ServerComplete **{locked_count}** Channel")

    @mod_server_lock.error
    async def mod_server_lock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ CommandManagePermission", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModServerLock(bot))
