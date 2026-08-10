import os
import json
import discord
from discord.ext import commands
from discord import app_commands

DATA_FILE = "jose_nicks.json"

class PermanentNick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.locked_nicks = self.load_data()

    def load_data(self):
        """從 jOSe 系統的 JSON 檔案中讀取永久暱稱資料"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    # JSON 的 key 預設是字串，我們需要把 guild_id 與 user_id 轉回整數 (int)
                    raw_data = json.load(f)
                    data = {}
                    for g_id, users in raw_data.items():
                        data[int(g_id)] = {int(u_id): nick for u_id, nick in users.items()}
                    return data
            except Exception as e:
                print(f"[jOSe系統] 讀取資料失敗: {e}")
        return {}

    def save_data(self):
        """將目前的永久暱稱資料寫入 jOSe 系統的 JSON 檔案中"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.locked_nicks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[jOSe系統] 儲存資料失敗: {e}")

    @app_commands.command(name="setpermanentnick", description="[jOSe系統] 設定某成員的永久暱稱（支援重啟持久化保存）")
    @app_commands.describe(member="要鎖定暱稱的成員", nickname="要強制套用的永久暱稱")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def setpermanentnick(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        guild_id = interaction.guild.id
        
        if guild_id not in self.locked_nicks:
            self.locked_nicks[guild_id] = {}
            
        # 記錄並持久化儲存
        self.locked_nicks[guild_id][member.id] = nickname
        self.save_data() # 立即寫入 jOSe 檔案
        
        try:
            await member.edit(nick=nickname, reason=f"由管理員 {interaction.user} 套用 jOSe 永久暱稱系統")
            
            embed = discord.Embed(
                title="🔒 jOSe 系統 - 永久暱稱已鎖定",
                description=f"成功將 **{member.mention}** 的暱稱鎖定為：\n`{nickname}`\n\n*✅ 此資料已寫入 jOSe 永久資料庫，機器人重啟後依然有效。*",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ 權限不足！我的身份組必須高於該成員，且擁有「管理暱稱」權限。", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 發生錯誤：{e}", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        guild_id = after.guild.id
        
        if guild_id not in self.locked_nicks:
            return
            
        if after.id not in self.locked_nicks[guild_id]:
            return
            
        target_nick = self.locked_nicks[guild_id][after.id]
        
        # 攔截違規改名並強制還原
        if after.display_name != target_nick:
            try:
                await after.edit(nick=target_nick, reason="[jOSe系統] 偵測到違規更改永久暱稱，系統自動還原")
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(PermanentNick(bot))