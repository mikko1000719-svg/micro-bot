# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import aiohttp
import re
from datetime import datetime
from discord import app_commands

class CPBL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ptt_url = "https://www.ptt.cc/bbs/Baseball/index.html"

    @commands.Cog.listener()
    async def on_ready(self):
        print("[OK] CPBL module loaded")

    # 斜線指令版本
    @app_commands.command(name="cpbl", description="查看中職比賽比分")
    async def cpbl_slash(self, interaction: discord.Interaction):
        """查看中職比賽比分（斜線指令版本）"""
        try:
            await interaction.response.defer(thinking=True)

            async with aiohttp.ClientSession() as session:
                async with session.get(self.ptt_url) as response:
                    if response.status == 200:
                        html = await response.text()

                        # 搜索中職相關標題
                        match = re.search(r'(中職|CPBL|中信|富邦|統一|樂天|味全)', html, re.IGNORECASE)

                        if match:
                            # 創建記分板風格的 Embed
                            embed = discord.Embed(
                                title="🏟️ 中職記分板",
                                description="中華職業棒球大聯盟",
                                color=discord.Color.blue()
                            )

                            # 添加模擬比賽信息（實際應該從 API 獲取）
                            embed.add_field(
                                name="📅 比賽日期",
                                value=datetime.now().strftime("%Y-%m-%d"),
                                inline=True
                            )
                            embed.add_field(
                                name="⏰ 更新時間",
                                value=datetime.now().strftime("%H:%M"),
                                inline=True
                            )

                            # 模擬比賽記分板
                            embed.add_field(
                                name="🎯 今日賽程",
                                value="```\n隊伍        1 2 3 4 5 6 7 8 9  R  H  E\n統一獅      0 0 0 0 0 0 0 0 0  0  0  0\n樂天桃猿    0 0 0 0 0 0 0 0 0  0  0  0\n\n中信兄弟    0 0 0 0 0 0 0 0 0  0  0  0\n富邦悍將    0 0 0 0 0 0 0 0 0  0  0  0\n```",
                                inline=False
                            )

                            embed.add_field(
                                name="📝 資訊來源",
                                value="[PTP 棒球版](https://www.ptt.cc/bbs/Baseball/)",
                                inline=False
                            )
                            embed.add_field(
                                name="⚠️ 注意",
                                value="此為示範數據，實時比分請查看官方網站",
                                inline=False
                            )
                            embed.set_footer(text="資料更新時間: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

                            await interaction.followup.send(embed=embed)
                        else:
                            await interaction.followup.send("📊 目前暫無中職相關資訊")
                    else:
                        await interaction.followup.send("❌ 無法連接到 PTP")
        except Exception as e:
            await interaction.followup.send(f"❌ 獲取資訊失敗: {e}")

    @app_commands.command(name="ptt", description="PTP 棒球版連結")
    async def ptt_slash(self, interaction: discord.Interaction):
        """PTP 棒球版連結（斜線指令版本）"""
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

        await interaction.response.send_message(embed=embed)

    # 傳統指令版本（prefix 指令）
    @commands.command(name='cpbl', aliases=['中職', '中職棒'])
    async def cpbl_scores(self, ctx):
        """查看中職比賽比分"""
        try:
            await ctx.send("📊 正在獲取中職比賽比分...")

            async with aiohttp.ClientSession() as session:
                async with session.get(self.ptt_url) as response:
                    if response.status == 200:
                        html = await response.text()

                        # 搜索中職相關標題
                        match = re.search(r'(中職|CPBL|中信|富邦|統一|樂天|味全)', html, re.IGNORECASE)

                        if match:
                            # 創建記分板風格的 Embed
                            embed = discord.Embed(
                                title="🏟️ 中職記分板",
                                description="中華職業棒球大聯盟",
                                color=discord.Color.blue()
                            )

                            # 添加模擬比賽信息
                            embed.add_field(
                                name="� 比賽日期",
                                value=datetime.now().strftime("%Y-%m-%d"),
                                inline=True
                            )
                            embed.add_field(
                                name="⏰ 更新時間",
                                value=datetime.now().strftime("%H:%M"),
                                inline=True
                            )

                            # 模擬比賽記分板
                            embed.add_field(
                                name="🎯 今日賽程",
                                value="```\n隊伍        1 2 3 4 5 6 7 8 9  R  H  E\n統一獅      0 0 0 0 0 0 0 0 0  0  0  0\n樂天桃猿    0 0 0 0 0 0 0 0 0  0  0  0\n\n中信兄弟    0 0 0 0 0 0 0 0 0  0  0  0\n富邦悍將    0 0 0 0 0 0 0 0 0  0  0  0\n```",
                                inline=False
                            )

                            embed.add_field(
                                name="�📝 資訊來源",
                                value="[PTP 棒球版](https://www.ptt.cc/bbs/Baseball/)",
                                inline=False
                            )
                            embed.add_field(
                                name="⚠️ 注意",
                                value="此為示範數據，實時比分請查看官方網站",
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
