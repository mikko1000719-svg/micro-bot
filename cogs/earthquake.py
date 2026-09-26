import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

class Earthquake(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # ReadSystem環境Variable中的 CWA_API_KEY
        self.cwa_key = os.getenv("CWA_API_KEY")

        if self.cwa_key:
            print("[OK] [地震Module] 中央氣象署 API 金鑰SettingsComplete！")
        else:
            print("[WARNING] [地震Module] 未偵測到 CWA_API_KEY 環境Variable！")

    @app_commands.command(name="地震", description="查詢最新顯著有感地震報告")
    async def earthquake_report(self, interaction: discord.Interaction):
        # 1. 立即回應 Discord 避免 3 秒超時
        try:
            await interaction.response.defer(thinking=True)
        except discord.errors.NotFound:
            return

        # 2. Check API Key
        if not self.cwa_key:
            await interaction.followup.send("[ERROR] Server尚未正確Settings `CWA_API_KEY`，請聯繫SystemManage員。")
            return

        # 3. 請求中央氣象署開放資料 (E-A0015-001 顯著有感地震資料)
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={self.cwa_key}&format=JSON"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        earthquakes = data.get("records", {}).get("Earthquake", [])

                        if not earthquakes:
                            await interaction.followup.send("[INFO] 目前沒有最新的地震報告資料。")
                            return

                        # 取得最新一筆地震資料
                        eq = earthquakes[0]
                        info = eq.get("EarthquakeInfo", {})
                        report_content = eq.get("ReportContent", "無詳細說明")
                        web_url = eq.get("Web", "https://www.cwa.gov.tw")

                        # 製作 Discord 內嵌卡片 (Embed)
                        embed = discord.Embed(
                            title=f"🔔 {eq.get('ReportTitle', '最新地震報告')}",
                            description=report_content,
                            color=discord.Color.red(),
                            url=web_url
                        )
                        embed.add_field(name="📅 發報時間", value=info.get("OriginTime", "未知"), inline=False)
                        embed.add_field(name="[LOCATION] 震央位置", value=info.get("Epicenter", {}).get("Location", "未知"), inline=True)
                        embed.add_field(name="💥 地震規模", value=f"M_L {info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', '未知')}", inline=True)
                        embed.add_field(name="📏 震源深度", value=f"{info.get('Depth', {}).get('Value', '未知')} 公里", inline=True)
                        embed.set_footer(text="資料來源：中華民國中央氣象署")

                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send(f"[ERROR] 存取氣象署 API Failed (HTTP 狀態碼: {resp.status})")
        except Exception as e:
            await interaction.followup.send(f"[ERROR] 查詢地震資料時發生未預期Error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Earthquake(bot))