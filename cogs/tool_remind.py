import discord
import asyncio
from discord.ext import commands
from discord import app_commands

class ToolRemind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="remind", description="設定一個計時提醒，時間到時機器人會私訊通知你")
    @app_commands.describe(minutes="幾分鐘後提醒", content="提醒內容")
    async def remind(self, interaction: discord.Interaction, minutes: int, content: str):
        if minutes < 1 or minutes > 1440:
            await interaction.response.send_message("❌ 提醒時間必須介於 1 到 1440 分鐘（24小時）之間！", ephemeral=True)
            return

        await interaction.response.send_message(f"⏰ 沒問題！我將在 **{minutes} 分鐘後**提醒你：`{content}`", ephemeral=True)

        # 非同步等待指定時間
        await asyncio.sleep(minutes * 60)

        try:
            embed = discord.Embed(title="⏰ 您的備忘提醒時間到囉！", description=content, color=discord.Color.gold())
            await interaction.user.send(embed=embed)
        except Exception:
            # 若使用者關閉私訊，改在原頻道標記提醒
            try:
                await interaction.channel.send(f"{interaction.user.mention} ⏰ 您的備忘提醒：{content}")
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(ToolRemind(bot))