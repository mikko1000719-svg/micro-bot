# -*- coding: utf-8 -*-
import os
import logging
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks

class KeepAlive(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Read Render 環境Variable；若未Settings則使用Default網址
        self.site_url = os.getenv("RENDER_EXTERNAL_URL", "https://micro-bot-1.onrender.com")
        # StartBackground Self-Ping 任務
        self.self_ping_task.start()

    def cog_unload(self):
        # 當Module卸載時Stop任務，防止Memory洩漏
        self.self_ping_task.cancel()

    # Settings每 10 分鐘AutoExecute一次，低於 Render 的 15 分鐘休眠Limit
    @tasks.loop(minutes=10)
    async def self_ping_task(self):
        if not self.site_url:
            logging.warning("[WARNING] [KeepAlive] Target URL not set, skipping Self-Ping.")
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.site_url, timeout=10) as resp:
                    if resp.status == 200:
                        logging.info(f"[OK] [KeepAlive] Successfully sent keep-alive request to {self.site_url} (HTTP 200)")
                    else:
                        logging.warning(f"[WARNING] [KeepAlive] Keep-alive request response abnormal: HTTP {resp.status}")
        except Exception as e:
            logging.error(f"[ERROR] [KeepAlive] Failed to send keep-alive request: {e}")

    @self_ping_task.before_loop
    async def before_self_ping(self):
        # 等待BotCompleteLogin後再開始任務
        await self.bot.wait_until_ready()

    @app_commands.command(name="keepalive", description="Check並觸發Bot防休眠保鮮狀態")
    async def keepalive(self, interaction: discord.Interaction):
        # 1. 立即延遲響應，避免 3 秒超時
        await interaction.response.defer(thinking=True)

        is_running = self.self_ping_task.is_running()
        status_text = "[OK] Keep-alive background task running" if is_running else "[STOP] Keep-alive background task stopped"
        latency = round(self.bot.latency * 1000)

        # 2. ManualSendTestConnection
        http_status = "未Test"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.site_url, timeout=5) as resp:
                    http_status = f"HTTP {resp.status}"
        except Exception as e:
            http_status = f"Failed ({e})"

        # 3. 建立Information面板
        embed = discord.Embed(
            title="[SHIELD] Bot 24/7 Anti-Sleep Diagnosis",
            color=discord.Color.green() if is_running else discord.Color.red()
        )
        embed.add_field(name="保鮮任務狀態", value=status_text, inline=False)
        embed.add_field(name="監控目標網址", value=f"`{self.site_url}`", inline=False)
        embed.add_field(name="Real-time網頁Test", value=f"`{http_status}`", inline=True)
        embed.add_field(name="WebSocket 延遲", value=f"`{latency} ms`", inline=True)

        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(KeepAlive(bot))