import discord
from discord.ext import commands
from discord import app_commands

class ModCreateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_create_channel", description="在伺服器中建立一個新的文字頻道")
    @app_commands.describe(name="頻道名稱")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_create_channel(self, interaction: discord.Interaction, name: str):
        try:
            guild = interaction.guild
            new_channel = await guild.create_text_channel(name=name, reason=f"由 {interaction.user} 建立")
            await interaction.response.send_message(f"[FOLDER] 成功建立文字頻道 {new_channel.mention}！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 建立頻道失敗：{e}", ephemeral=True)

    @mod_create_channel.error
    async def mod_create_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「管理員」權限才能使用此指令！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModCreateChannel(bot))
