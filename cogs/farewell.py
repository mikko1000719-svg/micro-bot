import os
import json
import discord
from discord import app_commands
from discord.ext import commands

# 設定儲存頻道資料的 JSON 檔案名稱
DATA_FILE = "farewell.json"

class Farewell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 機器人啟動時，自動載入已儲存的頻道資料
        self.channels = self.load_data()

    def load_data(self):
        """讀取 JSON 檔案中的頻道設定"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_data(self):
        """將目前的頻道設定寫入 JSON 檔案儲存"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.channels, f, indent=4)

    # --------------------------------------------------
    # 1. 斜線指令：設定道別通知頻道 (僅限管理員)
    # --------------------------------------------------
    @app_commands.command(name="set_farewell", description="設定成員退出通知的發送頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_farewell(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """
        參數說明：
        channel: 讓管理員選擇要發送道別訊息的目標文字頻道
        """
        guild_id = str(interaction.guild.id)
        # 將該伺服器的 ID 與對應的頻道 ID 記錄下來
        self.channels[guild_id] = channel.id
        self.save_data()
        
        # ephemeral=True 表示這則成功提示只有設定的管理員自己看得到
        await interaction.response.send_message(f"[OK] 成員退出通知頻道已成功設定為 {channel.mention}！", ephemeral=True)

    # --------------------------------------------------
    # 2. 斜線指令：手動說掰掰
    # --------------------------------------------------
    @app_commands.command(name="掰掰", description="跟伺服器的大家或特定成員說再見")
    async def bye(self, interaction: discord.Interaction, member: discord.Member = None):
        """
        參數說明：
        member: (可選) 選擇要特別說再見的伺服器成員
        """
        if member:
            message = f"👋 {interaction.user.mention} 依依不捨地跟 {member.mention} 說了掰掰！期待下次相見。"
        else:
            message = f"👋 {interaction.user.mention} 跟大家揮手說了掰掰！期待下次相見。"
            
        await interaction.response.send_message(message)

    # --------------------------------------------------
    # 3. 自動事件監聽：成員離開伺服器
    # --------------------------------------------------
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild_id = str(member.guild.id)
        
        # 檢查該伺服器是否有設定過道別頻道
        if guild_id in self.channels:
            # 透過 ID 取得頻道物件
            channel = self.bot.get_channel(self.channels[guild_id])
            if channel:
                # 建立一張美觀的 Embed 卡片來顯示道別訊息
                embed = discord.Embed(
                    title="🛫 成員離開",
                    description=f"**{member.name}** 離開了伺服器，祝他一切順利。",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=embed)

# 讓 main.py 能夠載入這個模組的設定函數
async def setup(bot):
    await bot.add_cog(Farewell(bot))