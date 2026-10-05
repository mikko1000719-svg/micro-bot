# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import aiohttp
import re
from datetime import datetime

class CPBL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ptt_url = "https://www.ptt.cc/bbs/Baseball/index.html"

    @commands.Cog.listener()
    async def on_ready(self):
        print("[OK] CPBL module loaded")

    @commands.command(name='cpbl', aliases=['中職', '中職棒'])
    async def cpbl_scores(self, ctx):
        """查看中職比賽資訊"""
        try:
            await ctx.send("📊 正在獲取中職比賽資訊...")

            async with aiohttp.ClientSession() as session:
                async with session.get(self.ptt_url) as response:
                    if response.status == 200:
                        html = await response.text()

                        # 簡單解析 PTP 棒球版內容
                        # 查找比賽相關的標題
                        match = re.search(r'(中職|CPBL|中信|富邦|統一|樂天|味全)', html, re.IGNORECASE)

                        if match:
                            embed = discord.Embed(
                                title="🏟️ 中職比賽資訊",
                                description="來自 PTP 棒球版",
                                color=discord.Color.blue()
                            )
                            embed.add_field(
                                name="📝 資訊來源",
                                value="PTP 棒球版 (https://www.ptt.cc/bbs/Baseball/)",
                                inline=False
                            )
                            embed.add_field(
                                name="⚠️ 注意",
                                value="此功能為簡化版本，如需詳細資訊請查看 PTP 棒球版",
                                inline=False
                            )
                            embed.set_footer(text="資料更新時間: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

                            await ctx.send(embed=embed)
                        else:
                            await ctx.send("📊 目前暫無中職相關資訊")
                    else:
                        await ctx.send("❌ 無法連接到 PTP")
        except Exception as e:
            await ctx.send(f"❌ 獲取資訊失敗: {e}")

    @commands.command(name='ptt', aliases=['批踢'])
    async def ptt_baseball(self, ctx):
        """PTP 棒球版連結"""
        embed = discord.Embed(
            title="🏟️ PTP 棒球版",
            description="點擊下方連結前往 PTP 棒球版",
            color=discord.Color.blue(),
            url="https://www.ptt.cc/bbs/Baseball/"
        )
        embed.add_field(
            name="🔗 連結",
            value="[PTP 棒球版](https://www.ptt.cc/bbs/Baseball/)",
            inline=False
        )
        embed.set_footer(text="點擊標題直接前往")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CPBL(bot))
