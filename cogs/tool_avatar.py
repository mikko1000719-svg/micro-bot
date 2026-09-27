import discord
from discord.ext import commands
from discord import app_commands

class ToolAvatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Command description")
    @app_commands.describe(member=" ()")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        embed = discord.Embed(title=f" {target.display_name} ", color=target.color)
        embed.set_image(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ToolAvatar(bot))