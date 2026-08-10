import discord
import random
from discord.ext import commands
from discord import app_commands

class GhostCardView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.current = player1
        self.ghost_slot = random.randint(1, 4)
        self.step = 1

    @discord.ui.button(label="🃏 抽取一張卡牌", style=discord.ButtonStyle.danger)
    async def draw_ghost(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current:
            await interaction.response.send_message("還沒輪到你抽牌！", ephemeral=True)
            return

        if self.step == self.ghost_slot:
            for child in self.children: child.disabled = True
            loser = self.current
            winner = self.player2 if loser == self.player1 else self.player1
            msg = f"👻 **抽到鬼牌了！** {loser.mention} 抽中了恐怖鬼牌！\n🎉 恭喜 {winner.mention} 獲勝！"
            await interaction.response.edit_message(content=msg, view=self)
        else:
            self.step += 1
            self.current = self.player2 if self.current == self.player1 else self.player1
            msg = f"🃏 **抽鬼牌對決**\n安全過關！抽到安全牌。\n現在輪到 {self.current.mention} 抽牌！"
            await interaction.response.edit_message(content=msg, view=self)

class GameGhostCard(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_ghostcard", description="輪流抽牌，看誰會抽到鬼牌！")
    async def play_ghostcard(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = GhostCardView(interaction.user, opponent)
        await interaction.response.send_message(f"👻 **抽鬼牌對決開始**\n{interaction.user.mention} VS {opponent.mention}\n由 {interaction.user.mention} 先抽！", view=view)

async def setup(bot): await bot.add_cog(GameGhostCard(bot))