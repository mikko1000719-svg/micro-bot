import discord
from discord.ext import commands
from discord import app_commands

class ModCreateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_create_channel", description="ServerChannel")
    @app_commands.describe(name="Channel")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_create_channel(self, interaction: discord.Interaction, name: str):
        try:
            guild = interaction.guild
            new_channel = await guild.create_text_channel(name=name, reason=f" {interaction.user} ")
            await interaction.response.send_message(f"📁 SuccessChannel {new_channel.mention}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ ChannelFailed{e}", ephemeral=True)

    @mod_create_channel.error
    async def mod_create_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModCreateChannel(bot))
