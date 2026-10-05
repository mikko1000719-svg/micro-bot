import discord
from discord.ext import commands
from discord import app_commands

class ModDeleteRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_delete_role", description="刪除功能")
    @app_commands.describe(role="Delete")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_delete_role(self, interaction: discord.Interaction, role: discord.Role):
        try:
            role_name = role.name
            await role.delete(reason=f" {interaction.user} Delete")
            await interaction.response.send_message(f"🗑️ SuccessDelete`@{role_name}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ DeleteFailed{e}", ephemeral=True)

    @mod_delete_role.error
    async def mod_delete_role_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModDeleteRole(bot))
