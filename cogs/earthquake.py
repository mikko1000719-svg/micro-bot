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
            print("[OK] [Module]  API SettingsComplete")
        else:
            print("[WARNING] [Module]  CWA_API_KEY Variable")

    @app_commands.command(name="Parameter description", description="Command description")
    async def earthquake_report(self, interaction: discord.Interaction):
        # 1.  Discord  3 
        try:
            await interaction.response.defer(thinking=True)
        except discord.errors.NotFound:
            return

        # 2. Check API Key
        if not self.cwa_key:
            await interaction.followup.send("[ERROR] ServerSettings `CWA_API_KEY`SystemManage")
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
                            await interaction.followup.send("[INFO] ")
                            return

                        # 
                        eq = earthquakes[0]
                        info = eq.get("EarthquakeInfo", {})
                        report_content = eq.get("ReportContent", "")
                        web_url = eq.get("Web", "https://www.cwa.gov.tw")

                        #  Discord  (Embed)
                        embed = discord.Embed(
                            title=f" {eq.get('ReportTitle', '')}",
                            description=report_content,
                            color=discord.Color.red(),
                            url=web_url
                        )
                        embed.add_field(name=" ", value=info.get("OriginTime", ""), inline=False)
                        embed.add_field(name="[LOCATION] ", value=info.get("Epicenter", {}).get("Location", ""), inline=True)
                        embed.add_field(name=" ", value=f"M_L {info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', '')}", inline=True)
                        embed.add_field(name=" ", value=f"{info.get('Depth', {}).get('Value', '')} ", inline=True)
                        embed.set_footer(text="Parameter description")

                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send(f"[ERROR]  API Failed (HTTP : {resp.status})")
        except Exception as e:
            await interaction.followup.send(f"[ERROR] Error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Earthquake(bot))