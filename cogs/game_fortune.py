import discord
import random
from discord.ext import commands
from discord import app_commands

class FortuneView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.scores = {player1: None, player2: None}

    @discord.ui.button(label="✨ 測驗今日幸運指數", style=discord.ButtonStyle.success)
    async def test_fortune(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的遊戲！", ephemeral=True)
            return
        if self.scores[interaction.user] is not None:
            await interaction.response.send_message("你已經測驗過了！", ephemeral=True)
            return

        score = random.randint(1, 100)
        self.scores[interaction.user] = score
        await interaction.response.send_message(f"測驗Complete！幸運指數：**{score}** 分！等待對手...", ephemeral=True)

        if self.scores[self.player1] is not None and self.scores[self.player2] is not None:
            button.disabled = True
            p1_s = self.scores[self.player1]
            p2_s = self.scores[self.player2]
            
            res = f"✨ **幸運指數結算**\n{self.player1.mention}：**{p1_s}** 分\n{self.player2.mention}：**{p2_s}** 分\n\n"
            if p1_s > p2_s: res += f"[TROPHY] 恭喜 {self.player1.mention} 運氣較好獲勝！"
            elif p2_s > p1_s: res += f"[TROPHY] 恭喜 {self.player2.mention} 運氣較好獲勝！"
            else: res += "[HANDSHAKE] 雙方幸運指數相同，平手！"

            await interaction.message.edit(content=res, view=self)

class GameFortune(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_fortune", description="測驗今日幸運指數比大小！")
    async def play_fortune(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = FortuneView(interaction.user, opponent)
        await interaction.response.send_message(f"✨ **幸運指數對決**\n{interaction.user.mention} VS {opponent.mention}\n請雙方測驗幸運指數！", view=view)

async def setup(bot): await bot.add_cog(GameFortune(bot))