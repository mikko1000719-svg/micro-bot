import discord
from discord.ext import commands
from discord import app_commands

class ModCreateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_create_channel", description="在Server中建立一個新的文字Channel")
    @app_commands.describe(name="Channel名稱")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_create_channel(self, interaction: discord.Interaction, name: str):
        try:
            guild = interaction.guild
            new_channel = await guild.create_text_channel(name=name, reason=f"由 {interaction.user} 建立")
            await interaction.response.send_message(f"[FOLDER] Success建立文字Channel {new_channel.mention}！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 建立ChannelFailed：{e}", ephemeral=True)

    @mod_create_channel.error
    async def mod_create_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModCreateChannel(bot))
