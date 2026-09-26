import discord
from discord.ext import commands
from discord import app_commands

class ModCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_check", description="CheckChannelPermission")
    @app_commands.describe(member="Check")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mod_check(self, interaction: discord.Interaction, member: discord.Member):
        channel = interaction.channel
        permissions = channel.permissions_for(member)
        
        embed = discord.Embed(title=f"[SHIELD] PermissionCheck{member.display_name}", color=discord.Color.blue())
        embed.add_field(name="SendMessage", value="[OK] " if permissions.send_messages else "[ERROR] ", inline=True)
        embed.add_field(name="", value="[OK] " if permissions.embed_links else "[ERROR] ", inline=True)
        embed.add_field(name="AdditionalFile", value="[OK] " if permissions.attach_files else "[ERROR] ", inline=True)
        embed.add_field(name="", value="[OK] " if permissions.add_reactions else "[ERROR] ", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @mod_check.error
    async def mod_check_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] PermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModCheck(bot))