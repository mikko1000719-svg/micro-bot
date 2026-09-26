import discord
import random
from discord.ext import commands
from discord import app_commands

class RouletteView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.bullet_chamber = random.randint(1, 6)
        self.current_chamber = 1

    @discord.ui.button(label="🔫 扣動扳機", style=discord.ButtonStyle.danger)
    async def pull_trigger(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current_player:
            await interaction.response.send_message("還沒輪到你喔！", ephemeral=True)
            return

        if self.current_chamber == self.bullet_chamber:
            button.disabled = True
            winner = self.player2 if self.current_player == self.player1 else self.player1
            msg = f"💥 **砰！**\n{self.current_player.mention} 中彈了！\n[PARTY] 恭喜 {winner.mention} 存活並獲得勝利！"
            await interaction.response.edit_message(content=msg, view=self)
        else:
            self.current_chamber += 1
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            msg = f"💨 **喀啦！** (空槍)\n運氣不錯，這發沒有子彈。\n現在輪到 {self.current_player.mention} 扣扳機！"
            await interaction.response.edit_message(content=msg, view=self)

class GameRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_roulette", description="與另一位玩家進行俄羅斯輪盤對戰！")
    async def play_roulette(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實的其他玩家！", ephemeral=True)
            return
            
        view = RouletteView(interaction.user, opponent)
        await interaction.response.send_message(f"🔫 **俄羅斯輪盤**\n{interaction.user.mention} VS {opponent.mention}\n子彈已上膛。由 {interaction.user.mention} 先開槍！", view=view)

async def setup(bot):
    await bot.add_cog(GameRoulette(bot))