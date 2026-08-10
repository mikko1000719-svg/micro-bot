import discord
import random
from discord.ext import commands
from discord import app_commands

class ToolChoose(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="choose", description="從多個選項中隨機挑選一個")
    @app_commands.describe(options="請輸入選項，用空格或逗號隔開")
    async def choose(self, interaction: discord.Interaction, options: str):
        raw_list = options.replace("，", ",").replace(" ", ",")
        choices = [item.strip() for item in raw_list.split(",") if item.strip()]
        if len(choices) < 2:
            await interaction.response.send_message("❌ 請至少提供兩個選項！", ephemeral=True)
            return
        selected = random.choice(choices)
        embed = discord.Embed(title="🎲 隨機選擇結果", color=discord.Color.purple())
        embed.add_field(name="選項清單", value="、".join(choices), inline=False)
        embed.add_field(name="最終決定", value=f"🎯 **{selected}**", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ToolChoose(bot))