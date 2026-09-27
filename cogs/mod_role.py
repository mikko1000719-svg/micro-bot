import discord
from discord.ext import commands
from discord import app_commands

class ModRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="role_add", description="Command description")
    @app_commands.describe(member="Parameter description", role="Parameter description")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def role_add(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message("❌ Failed", ephemeral=True)
            return

        try:
            await member.add_roles(role, reason=f"Manage {interaction.user} Command")
            await interaction.response.send_message(f"✅ Success {role.mention}  {member.mention}")
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed{e}", ephemeral=True)

    @app_commands.command(name="role_remove", description="Command description")
    @app_commands.describe(member="Parameter description", role="Parameter description")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def role_remove(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message("❌ Failed", ephemeral=True)
            return

        try:
            await member.remove_roles(role, reason=f"Manage {interaction.user} Command")
            await interaction.response.send_message(f"✅ Success {member.mention}  {role.mention}")
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed{e}", ephemeral=True)

    @role_add.error
    @role_remove.error
    async def mod_role_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModRole(bot))
