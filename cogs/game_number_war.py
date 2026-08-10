import discord
import random
from discord.ext import commands
from discord import app_commands

class NumberWarView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.scores = {player1: None, player2: None}

    @discord.ui.button(label="⚔️ 抽取戰鬥數字 (1-100)", style=discord.ButtonStyle.primary)
    async def draw_number(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的遊戲！", ephemeral=True)
            return
        if self.scores[interaction.user] is not None:
            await interaction.response.send_message("你已經抽取過數字了！", ephemeral=True)
            return

        num = random.randint(1, 100)
        self.scores[interaction.user] = num
        await interaction.response.send_message(f"你抽到的數字是 **{num}**！等待對手...", ephemeral=True)

        if self.scores[self.player1] is not None and self.scores[self.player2] is not None:
            button.disabled = True
            p1_s = self.scores[self.player1]
            p2_s = self.scores[self.player2]
            
            res = f"⚔️ **數字戰爭結算**\n{self.player1.mention}：**{p1_s}** 點\n{self.player2.mention}：**{p2_s}** 點\n\n"
            if p1_s > p2_s: res += f"🎉 恭喜 {self.player1.mention} 獲勝！"
            elif p2_s > p1_s: res += f"🎉 恭喜 {self.player2.mention} 獲勝！"
            else: res += "🤝 雙方點數相同，平手！"

            await interaction.message.edit(content=res, view=self)

class GameNumberWar(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_numberwar", description="抽取 1-100 數字進行對決！")
    async def play_numberwar(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = NumberWarView(interaction.user, opponent)
        await interaction.response.send_message(f"⚔️ **數字戰爭**\n{interaction.user.mention} VS {opponent.mention}\n請雙方點擊按鈕抽取數字！", view=view)

async def setup(bot): await bot.add_cog(GameNumberWar(bot))