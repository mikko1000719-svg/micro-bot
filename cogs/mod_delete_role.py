import discord
from discord.ext import commands
from discord import app_commands

class ModDeleteRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_delete_role", description="Delete指定的Server身分組")
    @app_commands.describe(role="要Delete的身分組")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_delete_role(self, interaction: discord.Interaction, role: discord.Role):
        try:
            role_name = role.name
            await role.delete(reason=f"由 {interaction.user} Delete")
            await interaction.response.send_message(f"[TRASH] SuccessDelete身分組：`@{role_name}`", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] Delete身分組Failed：{e}", ephemeral=True)

    @mod_delete_role.error
    async def mod_delete_role_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModDeleteRole(bot))
