import discord
from discord import app_commands
from discord.ext import commands
import os

class CloudCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="env_check", description="Check bot environment")
    async def env_check(self, interaction: discord.Interaction):
        # Send response
        try:
            await interaction.response.defer(thinking=True)
        except discord.errors.NotFound:
            return

        # Check environment variables
        # Render automatically sets "RENDER" variable
        is_render = os.environ.get("RENDER") is not None
        
        if is_render:
            status_msg = " **** Render ServerExecute"
        else:
            status_msg = "💻 ****Execute"

        #  3
        try:
            await interaction.followup.send(status_msg)
        except Exception as e:
            print(f"Failed: {e}")

async def setup(bot):
    await bot.add_cog(CloudCheck(bot))