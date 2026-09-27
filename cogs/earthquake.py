import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

class Earthquake(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # ReadSystemVariable CWA_API_KEY
        self.cwa_key = os.getenv("CWA_API_KEY")

        if self.cwa_key:
            print("[OK] [Module] CWA API Settings Complete")
        else:
            print("[WARNING] [Module] CWA_API_KEY Variable not found")

    @app_commands.command(name="earthquake", description="Get earthquake report")
    async def earthquake_report(self, interaction: discord.Interaction):
        # 1. Send defer response to avoid Discord timeout
        try:
            await interaction.response.defer(thinking=True)
        except discord.errors.NotFound:
            return

        # 2. Check API Key
        if not self.cwa_key:
            await interaction.followup.send("❌ ServerSettings `CWA_API_KEY`SystemManage")
            return

        # 3.  (E-A0015-001 )
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={self.cwa_key}&format=JSON"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        earthquakes = data.get("records", {}).get("Earthquake", [])

                        if not earthquakes:
                            await interaction.followup.send("ℹ️ ")
                            return

                        # 
                        eq = earthquakes[0]
                        info = eq.get("EarthquakeInfo", {})
                        report_content = eq.get("ReportContent", "")
                        web_url = eq.get("Web", "https://www.cwa.gov.tw")

                        # Send Discord response (Embed)
                        embed = discord.Embed(
                            title=f"🌋 {eq.get('ReportTitle', '')}",
                            description=report_content,
                            color=discord.Color.red(),
                            url=web_url
                        )
                        embed.add_field(name="⏰ Time", value=info.get("OriginTime", ""), inline=False)
                        embed.add_field(name="📍 Location", value=info.get("Epicenter", {}).get("Location", ""), inline=True)
                        embed.add_field(name="💪 Magnitude", value=f"M_L {info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', '')}", inline=True)
                        embed.add_field(name="📏 Depth", value=f"{info.get('Depth', {}).get('Value', '')} km", inline=True)
                        embed.set_footer(text="Taiwan Earthquake Report")

                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send(f"❌ API Failed (HTTP Status: {resp.status})")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Earthquake(bot))