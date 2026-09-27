import discord
from discord.ext import commands
from discord import app_commands

class ModDeleteChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_delete_channel", description="DeleteChannel")
    @app_commands.describe(channel="DeleteChannel (DeleteChannel)")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_delete_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        target_channel = channel or interaction.channel
        try:
            channel_name = target_channel.name
            await target_channel.delete(reason=f" {interaction.user} Delete")
            await interaction.response.send_message(f"🗑️ SuccessDeleteChannel`#{channel_name}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ DeleteChannelFailed{e}", ephemeral=True)

    @mod_delete_channel.error
    async def mod_delete_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModDeleteChannel(bot))
