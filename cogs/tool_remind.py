import discord
import asyncio
from discord.ext import commands
from discord import app_commands

class ToolRemind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="remind", description="設置功能")
    @app_commands.describe(minutes="Parameter description", content="Parameter description")
    async def remind(self, interaction: discord.Interaction, minutes: int, content: str):
        if minutes < 1 or minutes > 1440:
            await interaction.response.send_message("❌  1  1440 24", ephemeral=True)
            return

        await interaction.response.send_message(f"⏰  **{minutes} **`{content}`", ephemeral=True)

        # Sync
        await asyncio.sleep(minutes * 60)

        try:
            embed = discord.Embed(title="⏰ ", description=content, color=discord.Color.gold())
            await interaction.user.send(embed=embed)
        except Exception:
            # Channel
            try:
                await interaction.channel.send(f"{interaction.user.mention} ⏰ {content}")
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(ToolRemind(bot))