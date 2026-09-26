import discord
from discord import app_commands
from discord.ext import commands
import os

class CloudCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="", description="CheckBotRun")
    async def env_check(self, interaction: discord.Interaction):
        #  1Send 3 
        try:
            await interaction.response.defer(thinking=True)
        except discord.errors.NotFound:
            return

        #  2Variable
        # Render DefaultAuto "RENDER" Variable
        is_render = os.environ.get("RENDER") is not None
        
        if is_render:
            status_msg = " **** Render ServerExecute"
        else:
            status_msg = "[COMPUTER] ****Execute"

        #  3
        try:
            await interaction.followup.send(status_msg)
        except Exception as e:
            print(f"Failed: {e}")

async def setup(bot):
    await bot.add_cog(CloudCheck(bot))