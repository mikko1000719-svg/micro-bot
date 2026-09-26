import discord
from discord.ext import commands
from discord import app_commands

class ToolUserAvatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="useravatar", description="")
    @app_commands.describe(member=" ()")
    async def useravatar(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        avatar_url = target.display_avatar.url

        embed = discord.Embed(title=f" {target.display_name} ", color=target.color)
        embed.set_image(url=avatar_url)
        embed.description = f"[Graph]({avatar_url})"
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ToolUserAvatar(bot))