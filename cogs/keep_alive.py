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
        # Read Render VariableSettingsDefault
        self.site_url = os.getenv("RENDER_EXTERNAL_URL", "https://micro-bot-1.onrender.com")
        # StartBackground Self-Ping 
        self.self_ping_task.start()

    def cog_unload(self):
        # ModuleStopMemory
        self.self_ping_task.cancel()

    # Settings 10 AutoExecute Render  15 Limit
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
        # BotCompleteLogin
        await self.bot.wait_until_ready()

    @app_commands.command(name="keepalive", description="CheckBot")
    async def keepalive(self, interaction: discord.Interaction):
        # 1.  3 
        await interaction.response.defer(thinking=True)

        is_running = self.self_ping_task.is_running()
        status_text = "[OK] Keep-alive background task running" if is_running else "[STOP] Keep-alive background task stopped"
        latency = round(self.bot.latency * 1000)

        # 2. ManualSendTestConnection
        http_status = "Test"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.site_url, timeout=5) as resp:
                    http_status = f"HTTP {resp.status}"
        except Exception as e:
            http_status = f"Failed ({e})"

        # 3. Information
        embed = discord.Embed(
            title="[SHIELD] Bot 24/7 Anti-Sleep Diagnosis",
            color=discord.Color.green() if is_running else discord.Color.red()
        )
        embed.add_field(name="", value=status_text, inline=False)
        embed.add_field(name="", value=f"`{self.site_url}`", inline=False)
        embed.add_field(name="Real-timeTest", value=f"`{http_status}`", inline=True)
        embed.add_field(name="WebSocket ", value=f"`{latency} ms`", inline=True)

        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(KeepAlive(bot))