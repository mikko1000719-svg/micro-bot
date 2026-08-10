import os
import logging
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks

class KeepAlive(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 讀取 Render 環境變數；若未設定則使用預設網址
        self.site_url = os.getenv("RENDER_EXTERNAL_URL", "https://micro-bot-1.onrender.com")
        # 啟動背景 Self-Ping 任務
        self.self_ping_task.start()

    def cog_unload(self):
        # 當模組卸載時停止任務，防止記憶體洩漏
        self.self_ping_task.cancel()

    # 設定每 10 分鐘自動執行一次，低於 Render 的 15 分鐘休眠限制
    @tasks.loop(minutes=10)
    async def self_ping_task(self):
        if not self.site_url:
            logging.warning("⚠️ [KeepAlive] 未設定目標網址，跳過 Self-Ping。")
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.site_url, timeout=10) as resp:
                    if resp.status == 200:
                        logging.info(f"🟢 [KeepAlive] 成功發送保鮮請求至 {self.site_url} (HTTP 200)")
                    else:
                        logging.warning(f"⚠️ [KeepAlive] 保鮮請求回應異常: HTTP {resp.status}")
        except Exception as e:
            logging.error(f"❌ [KeepAlive] 發送保鮮請求失敗: {e}")

    @self_ping_task.before_loop
    async def before_self_ping(self):
        # 等待機器人完成登入後再開始任務
        await self.bot.wait_until_ready()

    @app_commands.command(name="keepalive", description="檢查並觸發機器人防休眠保鮮狀態")
    async def keepalive(self, interaction: discord.Interaction):
        # 1. 立即延遲響應，避免 3 秒超時
        await interaction.response.defer(thinking=True)

        is_running = self.self_ping_task.is_running()
        status_text = "🟢 保鮮背景任務運作中" if is_running else "🔴 保鮮背景任務已停止"
        latency = round(self.bot.latency * 1000)

        # 2. 手動發送測試連線
        http_status = "未測試"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.site_url, timeout=5) as resp:
                    http_status = f"HTTP {resp.status}"
        except Exception as e:
            http_status = f"失敗 ({e})"

        # 3. 建立資訊面板
        embed = discord.Embed(
            title="🛡️ 機器人 24/7 防休眠診斷",
            color=discord.Color.green() if is_running else discord.Color.red()
        )
        embed.add_field(name="保鮮任務狀態", value=status_text, inline=False)
        embed.add_field(name="監控目標網址", value=f"`{self.site_url}`", inline=False)
        embed.add_field(name="即時網頁測試", value=f"`{http_status}`", inline=True)
        embed.add_field(name="WebSocket 延遲", value=f"`{latency} ms`", inline=True)

        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(KeepAlive(bot))