import discord
import random
from discord.ext import commands
from discord import app_commands

class DestinyWheelView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.points = {player1: None, player2: None}

    @discord.ui.button(label="🎡 旋轉命運輪盤", style=discord.ButtonStyle.primary)
    async def spin_destiny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的輪盤！", ephemeral=True)
            return
        if self.points[interaction.user] is not None:
            await interaction.response.send_message("你已經轉過了！", ephemeral=True)
            return

        pt = random.randint(1, 1000)
        self.points[interaction.user] = pt
        await interaction.response.send_message(f"輪盤指著：**{pt}** 點！等待對手...", ephemeral=True)

        if self.points[self.player1] is not None and self.points[self.player2] is not None:
            button.disabled = True
            p1_p = self.points[self.player1]
            p2_p = self.points[self.player2]
            
            res = f"🎡 **命運輪盤結算**\n{self.player1.mention} 獲得：**{p1_p}** 點\n{self.player2.mention} 獲得：**{p2_p}** 點\n\n"
            if p1_p > p2_p: res += f"🎉 恭喜 {self.player1.mention} 獲勝！"
            elif p2_p > p1_p: res += f"🎉 恭喜 {self.player2.mention} 獲勝！"
            else: res += "🤝 雙方同點數，平手！"

            await interaction.message.edit(content=res, view=self)

class GameDestinyWheel(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_destinywheel", description="旋轉命運輪盤進行點數對決！")
    async def play_destinywheel(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = DestinyWheelView(interaction.user, opponent)
        await interaction.response.send_message(f"🎡 **命運輪盤對決**\n{interaction.user.mention} VS {opponent.mention}\n請雙方旋轉輪盤！", view=view)

async def setup(bot): await bot.add_cog(GameDestinyWheel(bot))