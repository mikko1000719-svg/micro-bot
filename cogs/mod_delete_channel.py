import discord
from discord.ext import commands
from discord import app_commands

class ModDeleteChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_delete_channel", description="Delete指定的文字Channel")
    @app_commands.describe(channel="要Delete的文字Channel (留空則Delete目前Channel)")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_delete_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        target_channel = channel or interaction.channel
        try:
            channel_name = target_channel.name
            await target_channel.delete(reason=f"由 {interaction.user} Delete")
            await interaction.response.send_message(f"[TRASH] SuccessDelete文字Channel：`#{channel_name}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] DeleteChannelFailed：{e}", ephemeral=True)

    @mod_delete_channel.error
    async def mod_delete_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModDeleteChannel(bot))
