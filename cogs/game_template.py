import discord
import random
from discord.ext import commands
from discord import app_commands

class TemplateView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.ready = {player1: False, player2: False}

    @discord.ui.button(label="[DICE] 抽取結果", style=discord.ButtonStyle.primary)
    async def action_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            return
            
        self.ready[interaction.user] = True
        
        if self.ready[self.player1] and self.ready[self.player2]:
            button.disabled = True
            
            # --- 這裡是你自訂邏輯的地方 ---
            p1_score = random.randint(1, 10)
            p2_score = random.randint(1, 10)
            
            res = f"結果出爐：\n{self.player1.mention} 獲得 {p1_score}\n{self.player2.mention} 獲得 {p2_score}\n\n"
            if p1_score > p2_score: res += f"[TROPHY] {self.player1.mention} 贏了！"
            elif p2_score > p1_score: res += f"[TROPHY] {self.player2.mention} 贏了！"
            else: res += "[HANDSHAKE] 平手！"
            # -------------------------------
            
            await interaction.response.edit_message(content=res, view=self)
        else:
            await interaction.response.edit_message(content=f"[OK] {interaction.user.mention} 已準備！等待對手...")

class GameTemplate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_custom", description="自訂的抽卡/比大小對戰")
    async def play_custom(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = TemplateView(interaction.user, opponent)
        await interaction.response.send_message(f"⚔️ **自訂對戰**\n{interaction.user.mention} VS {opponent.mention}\n請點擊按鈕！", view=view)

async def setup(bot):
    await bot.add_cog(GameTemplate(bot))