import discord
from discord.ext import commands
from discord import app_commands

class ModUnlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_unlock", description="解鎖目前Channel，恢復一般成員發言Permission")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_unlock(self, interaction: discord.Interaction):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None  
        
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason=f"由 {interaction.user} 解鎖Channel")
            await interaction.response.send_message("[UNLOCK] 此Channel已解鎖，恢復正常發言。")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 解鎖ChannelFailed：{e}", ephemeral=True)

    @mod_unlock.error
    async def mod_unlock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModUnlock(bot))
