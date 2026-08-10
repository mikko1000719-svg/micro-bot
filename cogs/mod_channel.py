import discord
from discord.ext import commands
from discord import app_commands

class ModChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_setchannel", description="將目前頻道設定為伺服器公告專用頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def mod_setchannel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        target_channel = channel or interaction.channel
        await interaction.response.send_message(f"📢 成功將公告頻道綁定至 {target_channel.mention}！", ephemeral=True)

    @mod_setchannel.error
    async def mod_setchannel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「管理頻道」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModChannel(bot))