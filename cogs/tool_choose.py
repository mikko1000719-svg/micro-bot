import discord
import random
from discord.ext import commands
from discord import app_commands

class ToolChoose(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="choose", description="Option")
    @app_commands.describe(options="Option")
    async def choose(self, interaction: discord.Interaction, options: str):
        raw_list = options.replace("", ",").replace(" ", ",")
        choices = [item.strip() for item in raw_list.split(",") if item.strip()]
        if len(choices) < 2:
            await interaction.response.send_message("❌ Option", ephemeral=True)
            return
        selected = random.choice(choices)
        embed = discord.Embed(title="🎲 ", color=discord.Color.purple())
        embed.add_field(name="Option", value="Parameter description".join(choices), inline=False)
        embed.add_field(name="Parameter description", value=f"[TARGET] **{selected}**", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ToolChoose(bot))