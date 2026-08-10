import discord
import random
from discord.ext import commands
from discord import app_commands

class LuckyView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.current = player1
        self.trap = random.randint(1, 5)
        self.step = 1

    @discord.ui.button(label="🍀 拔取幸運草 (1~5)", style=discord.ButtonStyle.success)
    async def pick_clover(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current:
            await interaction.response.send_message("還沒輪到你喔！", ephemeral=True)
            return

        if self.step == self.trap:
            for child in self.children: child.disabled = True
            loser = self.current
            winner = self.player2 if loser == self.player1 else self.player1
            msg = f"💥 **踩到陷阱了！** {loser.mention} 拔到了毒草！\n🎉 恭喜 {winner.mention} 獲勝！"
            await interaction.response.edit_message(content=msg, view=self)
        else:
            self.step += 1
            self.current = self.player2 if self.current == self.player1 else self.player1
            msg = f"🍀 **幸運草對決**\n安全過關！目前進行到第 {self.step} 輪。\n現在輪到 {self.current.mention} 拔幸運草！"
            await interaction.response.edit_message(content=msg, view=self)

class GameLucky(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_lucky", description="輪流拔幸運草，看誰會踩到陷阱！")
    async def play_lucky(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = LuckyView(interaction.user, opponent)
        await interaction.response.send_message(f"🍀 **幸運草對決開始**\n{interaction.user.mention} VS {opponent.mention}\n由 {interaction.user.mention} 先開始！", view=view)

async def setup(bot): await bot.add_cog(GameLucky(bot))