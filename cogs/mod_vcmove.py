import discord
from discord.ext import commands
from discord import app_commands

class ModVCMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_vcmove", description="ChannelChannel")
    @app_commands.describe(member="Parameter description", target_channel="Channel")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_vcmove(self, interaction: discord.Interaction, member: discord.Member, target_channel: discord.VoiceChannel):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ Channel", ephemeral=True)
            return

        try:
            old_channel = member.voice.channel
            await member.move_to(target_channel, reason=f" {interaction.user} ")
            await interaction.response.send_message(
                f" Success {member.mention}  **{old_channel.name}**  **{target_channel.name}**",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed{e}", ephemeral=True)

    @mod_vcmove.error
    async def mod_vcmove_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModVCMove(bot))
