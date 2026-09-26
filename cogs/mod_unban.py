import discord
from discord.ext import commands
from discord import app_commands

class ModUnban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_unban", description=" ID ")
    @app_commands.describe(user_id=" ID (Number)", reason=" ()")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_unban(self, interaction: discord.Interaction, user_id: str, reason: str = "Manage"):
        try:
            user_obj = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user_obj, reason=reason)
            await interaction.response.send_message(f"[OK] Success `{user_obj.name}` ")
        except ValueError:
            await interaction.response.send_message("[ERROR] Number User ID", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] FailedUser{e}", ephemeral=True)

    @mod_unban.error
    async def mod_unban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModUnban(bot))
