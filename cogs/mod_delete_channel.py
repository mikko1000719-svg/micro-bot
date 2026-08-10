import discord
from discord.ext import commands
from discord import app_commands

class ModDeleteChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_delete_channel", description="刪除指定的文字頻道")
    @app_commands.describe(channel="要刪除的文字頻道 (留空則刪除目前頻道)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def mod_delete_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        target_channel = channel or interaction.channel
        try:
            channel_name = target_channel.name
            await target_channel.delete(reason=f"由 {interaction.user} 刪除")
            await interaction.response.send_message(f"🗑️ 成功刪除文字頻道：`#{channel_name}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 刪除頻道失敗：{e}", ephemeral=True)

    @mod_delete_channel.error
    async def mod_delete_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「管理頻道」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModDeleteChannel(bot))