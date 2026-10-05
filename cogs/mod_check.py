import discord
from discord.ext import commands
from discord import app_commands

class ModCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_check", description="檢查狀態")
    @app_commands.describe(member="Check")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mod_check(self, interaction: discord.Interaction, member: discord.Member):
        channel = interaction.channel
        permissions = channel.permissions_for(member)
        
        embed = discord.Embed(title=f"🛡️ PermissionCheck{member.display_name}", color=discord.Color.blue())
        embed.add_field(name="SendMessage", value="✅ " if permissions.send_messages else "❌ ", inline=True)
        embed.add_field(name="Parameter description", value="✅ " if permissions.embed_links else "❌ ", inline=True)
        embed.add_field(name="AdditionalFile", value="✅ " if permissions.attach_files else "❌ ", inline=True)
        embed.add_field(name="Parameter description", value="✅ " if permissions.add_reactions else "❌ ", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @mod_check.error
    async def mod_check_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ PermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModCheck(bot))