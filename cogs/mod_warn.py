import discord
from discord.ext import commands
from discord import app_commands

class ModWarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_warn", description="SendWarning")
    @app_commands.describe(member="Warning", reason="Warning")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            embed = discord.Embed(title="[WARNING] ServerWarning", color=discord.Color.orange())
            embed.description = f"Server **{interaction.guild.name}** ManageWarning"
            embed.add_field(name="", value=reason)
            await member.send(embed=embed)
            dm_status = "[OK] Success"
        except discord.Forbidden:
            dm_status = "[WARNING] Function"

        await interaction.response.send_message(f"  {member.mention} Warning\n****{reason}\n{dm_status}")

    @mod_warn.error
    async def mod_warn_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModWarn(bot))
