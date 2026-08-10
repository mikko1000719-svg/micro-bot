import os
import json
import discord
from discord import app_commands
from discord.ext import commands

DATA_FILE = "levels.json"

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_data = self.load_data()

    def load_data(self):
        """從 JSON 檔案載入經驗值數據"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"【等級系統】讀取 levels.json 失敗，初始化空資料: {e}")
                return {}
        return {}

    def save_data(self):
        """儲存經驗值數據至 JSON 檔案"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.xp_data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 忽略機器人訊息
        if message.author.bot:
            return

        user_id = str(message.author.id)
        # 每次發言經驗值 +1
        self.xp_data[user_id] = self.xp_data.get(user_id, 0) + 1
        self.save_data()

        xp = self.xp_data[user_id]
        level = int(xp**0.5) // 5

        # 每 25 點經驗值觸發升級通知
        if xp % 25 == 0:
            await message.channel.send(f"🎉 恭喜 {message.author.mention} 升級了！目前等級：{level} (總經驗值: {xp})")

    @app_commands.command(name="rank", description="查看自己的等級與經驗值")
    async def rank(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        xp = self.xp_data.get(user_id, 0)
        level = int(xp**0.5) // 5
        await interaction.response.send_message(f"📊 {interaction.user.name}，你的目前等級是 {level}，經驗值為 {xp}。", ephemeral=True)

async def setup(bot):
    """標準 Cog 載入入口點"""
    await bot.add_cog(Leveling(bot))