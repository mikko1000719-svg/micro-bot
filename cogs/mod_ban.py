import discord
from discord.ext import commands
from discord import app_commands

class ModBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_ban", description="Permanent (Ban)")
    @app_commands.describe(member="", reason=" ()")
    @app_commands.default_permissions(administrator=True) # HiddenCommand
    @app_commands.checks.has_permissions(administrator=True) # ManagePermission
    async def mod_ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = ""):
        if member == interaction.user:
            await interaction.response.send_message("！", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"🔨  {member.mention} Success。\n：{reason}")
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] Failed：{e}", ephemeral=True)

    @mod_ban.error
    async def mod_ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 「Manage」PermissionCommand！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModBan(bot))
