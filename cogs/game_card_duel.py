import discord
import random
from discord.ext import commands
from discord import app_commands

class CardDuelView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.cards = {player1: None, player2: None}

    @discord.ui.button(label="🎴 抽一張命運卡牌", style=discord.ButtonStyle.secondary)
    async def draw_card(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的牌局！", ephemeral=True)
            return
        if self.cards[interaction.user] is not None:
            await interaction.response.send_message("你已經抽過牌了！", ephemeral=True)
            return

        card_val = random.randint(1, 13)
        self.cards[interaction.user] = card_val
        await interaction.response.send_message(f"你抽到了點數 【{card_val}】 的卡牌！等待對手...", ephemeral=True)

        if self.cards[self.player1] is not None and self.cards[self.player2] is not None:
            button.disabled = True
            p1_c = self.cards[self.player1]
            p2_c = self.cards[self.player2]
            
            res = f"🎴 **卡牌決鬥結算**\n{self.player1.mention} 抽到：**{p1_c}**\n{self.player2.mention} 抽到：**{p2_c}**\n\n"
            if p1_c > p2_c: res += f"🏆 恭喜 {self.player1.mention} 獲勝！"
            elif p2_c > p1_c: res += f"🏆 恭喜 {self.player2.mention} 獲勝！"
            else: res += "🤝 雙方抽到相同點數，平手！"

            await interaction.message.edit(content=res, view=self)

class GameCardDuel(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_cardduel", description="抽取命運卡牌進行點數對決！")
    async def play_cardduel(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = CardDuelView(interaction.user, opponent)
        await interaction.response.send_message(f"🎴 **命運卡牌對決**\n{interaction.user.mention} VS {opponent.mention}\n請雙方抽取卡牌！", view=view)

async def setup(bot): await bot.add_cog(GameCardDuel(bot))