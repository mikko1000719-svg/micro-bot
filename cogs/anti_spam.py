import discord
from discord.ext import commands
from datetime import timedelta
from collections import defaultdict

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 紀錄Format: {user_id: {"content": 內容, "count": 重複次數, "burst": Message爆發量}}
        self.user_data = defaultdict(lambda: {"content": "", "count": 0, "burst": 0})

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild or message.author.guild_permissions.administrator:
            return

        user_id = message.author.id
        content = message.content.strip()
        data = self.user_data[user_id]

        # 1. 偵測重複言論 (三次禁言)
        if data["content"] == content:
            data["count"] += 1
        else:
            data["content"] = content
            data["count"] = 1

        if data["count"] >= 3:
            try:
                await message.author.timeout(timedelta(hours=24), reason="微國 5.0：重複洗頻達 3 次")
                await message.channel.send(f"🚨 {message.author.mention} 因為洗頻已被Auto禁言 24 小時。")
                data["count"] = 0 # 重置紀錄
            except Exception as e:
                print(f"禁言Failed: {e}")
                
        # 2. 偵測炸群行為 (例如短時間內Send過多Message)
        # 這裡您可以依據Requirement調整閾值，例如 5 秒內發超過 10 則
        data["burst"] += 1
        # 您可以在此加入對應的炸群Defense邏輯...

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))