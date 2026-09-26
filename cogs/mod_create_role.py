import discord
from discord.ext import commands
from discord import app_commands

class ModCreateRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_create_role", description="Server")
    @app_commands.describe(name="")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_create_role(self, interaction: discord.Interaction, name: str):
        try:
            guild = interaction.guild
            new_role = await guild.create_role(name=name, reason=f" {interaction.user} ")
            await interaction.response.send_message(f"🏷️ Success {new_role.mention}！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] Failed：{e}", ephemeral=True)

    @mod_create_role.error
    async def mod_create_role_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 「Manage」PermissionCommand！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModCreateRole(bot))
