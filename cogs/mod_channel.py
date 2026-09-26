import discord
from discord.ext import commands
from discord import app_commands

class ModChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_setchannel", description="將目前ChannelSettings為Server公告DedicatedChannel")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_setchannel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        target_channel = channel or interaction.channel
        await interaction.response.send_message(f"[SPEAKER] Success將公告Channel綁定至 {target_channel.mention}！", ephemeral=True)

    @mod_setchannel.error
    async def mod_setchannel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModChannel(bot))
