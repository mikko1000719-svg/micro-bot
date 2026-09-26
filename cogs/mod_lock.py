import discord
from discord.ext import commands
from discord import app_commands

class ModLock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_lock", description="鎖定目前頻道，禁止一般成員發言")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_lock(self, interaction: discord.Interaction):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason=f"由 {interaction.user} 鎖定頻道")
            await interaction.response.send_message("[LOCK] 此頻道已被成功鎖定，一般成員暫時無法發言。")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 鎖定頻道失敗：{e}", ephemeral=True)

    @mod_lock.error
    async def mod_lock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「管理員」權限才能使用此指令！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModLock(bot))
