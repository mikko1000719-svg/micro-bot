import discord
import random
from discord.ext import commands
from discord import app_commands

class BalloonView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.current = player1
        self.boom_balloon = random.randint(1, 4)
        self.step = 1

    @discord.ui.button(label="🎈 戳破一顆氣球", style=discord.ButtonStyle.danger)
    async def poke_balloon(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current:
            await interaction.response.send_message("還沒輪到你戳氣球！", ephemeral=True)
            return

        if self.step == self.boom_balloon:
            for child in self.children: child.disabled = True
            loser = self.current
            winner = self.player2 if loser == self.player1 else self.player1
            msg = f"💥 **砰！** {loser.mention} 戳到了會爆炸的氣球！\n[PARTY] 恭喜 {winner.mention} 獲得勝利！"
            await interaction.response.edit_message(content=msg, view=self)
        else:
            self.step += 1
            self.current = self.player2 if self.current == self.player1 else self.player1
            msg = f"🎈 **戳氣球對決**\nSecurity過關！氣球安然無恙。\n現在輪到 {self.current.mention} 戳氣球！"
            await interaction.response.edit_message(content=msg, view=self)

class GameBalloon(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_balloon", description="輪流戳氣球，看誰會讓氣球爆炸！")
    async def play_balloon(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = BalloonView(interaction.user, opponent)
        await interaction.response.send_message(f"🎈 **終極戳氣球開始**\n{interaction.user.mention} VS {opponent.mention}\n由 {interaction.user.mention} 先戳！", view=view)

async def setup(bot): await bot.add_cog(GameBalloon(bot))