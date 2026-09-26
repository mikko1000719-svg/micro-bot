import discord
import asyncio
import random
from discord.ext import commands
from discord import app_commands

class ReactionView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=60)
        self.players = [player1, player2]
        self.clicked = False

    @discord.ui.button(label="[BOLT] 點擊搶答！", style=discord.ButtonStyle.danger)
    async def click_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            await interaction.response.send_message("這不是你的比賽！", ephemeral=True)
            return
            
        if not self.clicked:
            self.clicked = True
            button.disabled = True
            button.style = discord.ButtonStyle.success
            await interaction.response.edit_message(content=f"[PARTY] 比賽結束！\n[BOLT] **{interaction.user.mention}** 的手速最快，獲得勝利！", view=self)

class GameReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_reaction", description="與對手比拼手速！")
    async def play_reaction(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return

        await interaction.response.send_message(f"[BOLT] {interaction.user.mention} VS {opponent.mention}\n**準備...** (按鈕隨時會出現)")
        
        # 隨機等待 2 到 6 秒
        await asyncio.sleep(random.uniform(2.0, 6.0))
        
        view = ReactionView(interaction.user, opponent)
        # 取得剛才發送的訊息並更新
        msg = await interaction.original_response()
        await msg.edit(content=f"🚨 **就是現在！快按！**\n{interaction.user.mention} VS {opponent.mention}", view=view)

async def setup(bot):
    await bot.add_cog(GameReaction(bot))