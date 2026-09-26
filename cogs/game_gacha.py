import discord
import random
from discord.ext import commands
from discord import app_commands

class GachaView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.cards = {player1: None, player2: None}

    @discord.ui.button(label="🎴 抽一張稀有卡", style=discord.ButtonStyle.primary)
    async def gacha_draw(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的抽卡局！", ephemeral=True)
            return
        if self.cards[interaction.user] is not None:
            await interaction.response.send_message("你已經抽過卡了！", ephemeral=True)
            return

        rarities = ["N", "R", "SR", "SSR"]
        weights = [50, 30, 15, 5]
        drawn = random.choices(rarities, weights=weights)[0]
        score_map = {"N": 1, "R": 2, "SR": 3, "SSR": 5}
        
        self.cards[interaction.user] = (drawn, score_map[drawn])
        await interaction.response.send_message(f"你抽到了【{drawn}】級卡牌！等待對手...", ephemeral=True)

        if self.cards[self.player1] is not None and self.cards[self.player2] is not None:
            button.disabled = True
            p1_name, p1_val = self.cards[self.player1]
            p2_name, p2_val = self.cards[self.player2]
            
            res = f"🎴 **抽卡對決結算**\n{self.player1.mention} 抽到：{p1_name}\n{self.player2.mention} 抽到：{p2_name}\n\n"
            if p1_val > p2_val: res += f"[PARTY] 恭喜 {self.player1.mention} 抽到較稀有的卡片獲勝！"
            elif p2_val > p1_val: res += f"[PARTY] 恭喜 {self.player2.mention} 抽到較稀有的卡片獲勝！"
            else: res += "[HANDSHAKE] 雙方抽到同等級卡片，平手！"

            await interaction.message.edit(content=res, view=self)

class GameGacha(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_gacha", description="抽取稀有卡牌進行對決！")
    async def play_gacha(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = GachaView(interaction.user, opponent)
        await interaction.response.send_message(f"🎴 **抽卡對決開始**\n{interaction.user.mention} VS {opponent.mention}\n請雙方抽取卡牌！", view=view)

async def setup(bot): await bot.add_cog(GameGacha(bot))