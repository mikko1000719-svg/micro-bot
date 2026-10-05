import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class ModManage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mute", description="指令說明")
    @app_commands.describe(member="Parameter description", minutes="Parameter description", reason="Parameter description")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = ""):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ ", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            embed = discord.Embed(
                title=" Success",
                description=f"Success {member.mention} **{minutes} **\n`{reason}`",
                color=discord.Color.orange()
            )
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"❌ ExecuteFailed{e}", ephemeral=True)

    @app_commands.command(name="unmute", description="指令說明")
    @app_commands.describe(member="Parameter description")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        try:
            await member.timeout(None, reason="Parameter description")
            embed = discord.Embed(
                title=" ",
                description=f"Success {member.mention} Limit",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ ExecuteFailed{e}", ephemeral=True)

    # ErrorProcess
    @mute.error
    @unmute.error
    async def mod_manage_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModManage(bot))
