import os
import json
import asyncio
import discord
from discord.ext import commands

CONFIG_FILE = "bot_owner.json"

class OwnerDM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = self.load_owner_id()
        self.latest_error = "[OK] 無系統錯誤" # 紀錄最新的系統錯誤狀況

    def load_owner_id(self):
        """從 JSON 檔案中載入擁有者 ID"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("owner_id")
            except Exception as e:
                print(f"[微國機器人 5.0] 讀取 Owner 配置失敗: {e}")
        return None

    def save_owner_id(self, user_id: int):
        """將擁有者 ID 持久化儲存至 JSON 檔案"""
        self.owner_id = user_id
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"owner_id": user_id}, f, ensure_ascii=False, indent=4)
            print(f"[微國機器人 5.0] 成功綁定唯一操控者 ID: {user_id}")
        except Exception as e:
            print(f"[微國機器人 5.0] 儲存 Owner 配置失敗: {e}")

    def log_error(self, error_msg: str):
        """供全域呼叫的錯誤記錄器"""
        self.latest_error = f"[STOP] 最近錯誤: {error_msg}"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 忽略機器人自身的訊息
        if message.author.bot:
            return

        # 只處理「私訊 (DMChannel)」
        if isinstance(message.channel, discord.DMChannel):
            user_id = message.author.id

            # 首次設定擁有者（如果尚未設定）
            if self.owner_id is None:
                self.save_owner_id(user_id)
                await message.channel.send(f"👑 身份驗證成功！您已登記為 **微國機器人 5.0** 的唯一操控者。")
                return

            # 如果發送者不是唯一操控者
            if user_id != self.owner_id:
                await message.channel.send("[ERROR] 你不是微國機器人 5.0 的唯一操控者，無法存取控制面板。")
                return

            # === 擁有者私訊觸發：回傳系統狀態與伺服器列表 ===
            await message.channel.send("[SWITCH] 正在讀取伺服器狀態與生成邀請連結，請稍候...")

            embed = discord.Embed(
                title="[SHIELD] 微國機器人 5.0 - 操控者控制面板",
                description=f"**當前系統狀態**：{self.latest_error}\n**連線延遲 (Ping)**：`{round(self.bot.latency * 1000)} ms`\n**服務伺服器總數**：`{len(self.bot.guilds)}` 個",
                color=discord.Color.blue()
            )

            guild_info_list = []
            for guild in self.bot.guilds:
                invite_url = "無法建立邀請"
                
                # 嘗試尋找可發送邀請的文字頻道，避開 API Rate Limit (429)
                try:
                    for channel in guild.text_channels:
                        if channel.permissions_for(guild.me).create_instant_invite:
                            invite = await channel.create_invite(max_age=3600, max_uses=5, reason="微國機器人操控者面板生成")
                            invite_url = invite.url
                            break
                except Exception:
                    pass

                guild_info_list.append(f"• **{guild.name}** (ID: `{guild.id}`)\n  成員數: {guild.member_count} | [點此進入伺服器]({invite_url})")
                
                # 關鍵防護：微短延遲，防止短時間呼叫 API 造成 429 錯誤
                await asyncio.sleep(0.2)

            # 分頁處理（防止 Discord 訊息長度超過 4000 字元限制）
            guild_chunks = [guild_info_list[i:i + 5] for i in range(0, len(guild_info_list), 5)]
            
            for index, chunk in enumerate(guild_chunks):
                field_title = "🏰 伺服器列表與邀請連結" if index == 0 else f"🏰 伺服器列表 (頁次 {index + 1})"
                embed.add_field(name=field_title, value="\n".join(chunk), inline=False)

            await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OwnerDM(bot))
