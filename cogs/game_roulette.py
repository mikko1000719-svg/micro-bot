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

    @discord.ui.button(label="🔫 ", style=discord.ButtonStyle.danger)
    async def pull_trigger(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current_player:
            await interaction.response.send_message("！", ephemeral=True)
            return

        if self.current_chamber == self.bullet_chamber:
            button.disabled = True
            winner = self.player2 if self.current_player == self.player1 else self.player1
            msg = f"💥 **！**\n{self.current_player.mention} ！\n[PARTY]  {winner.mention} ！"
            await interaction.response.edit_message(content=msg, view=self)
        else:
            self.current_chamber += 1
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            msg = f"💨 **！** ()\n，。\n {self.current_player.mention} ！"
            await interaction.response.edit_message(content=msg, view=self)

class GameRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_roulette", description="！")
    async def play_roulette(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("！", ephemeral=True)
            return
            
        view = RouletteView(interaction.user, opponent)
        await interaction.response.send_message(f"🔫 ****\n{interaction.user.mention} VS {opponent.mention}\n。 {interaction.user.mention} ！", view=view)

async def setup(bot):
    await bot.add_cog(GameRoulette(bot))