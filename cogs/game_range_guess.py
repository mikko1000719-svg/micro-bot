import discord
import random
from discord.ext import commands
from discord import app_commands

class RangeGuessView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.current = player1
        self.target = random.randint(1, 50)
        self.min_v = 1
        self.max_v = 50

    @discord.ui.button(label="[TARGET] Number", style=discord.ButtonStyle.primary)
    async def guess(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current:
            await interaction.response.send_message("", ephemeral=True)
            return

        guess_val = random.randint(self.min_v, self.max_v)
        if guess_val == self.target or self.min_v >= self.max_v - 1:
            for child in self.children: child.disabled = True
            loser = self.current
            winner = self.player2 if loser == self.player1 else self.player1
            msg = f" **** {loser.mention} Number **{self.target}**\n[PARTY]  {winner.mention} "
            await interaction.response.edit_message(content=msg, view=self)
        else:
            if guess_val > self.target: self.max_v = guess_val
            else: self.min_v = guess_val
            self.current = self.player2 if self.current == self.player1 else self.player1
            msg = f"[TARGET] **Number**\n**{self.min_v} ~ {self.max_v}**\n {self.current.mention} "
            await interaction.response.edit_message(content=msg, view=self)

class GameRangeGuess(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_rangeguess", description="Number")
    async def play_rangeguess(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
        view = RangeGuessView(interaction.user, opponent)
        await interaction.response.send_message(f"[TARGET] **Number**\n{interaction.user.mention} VS {opponent.mention}\n {interaction.user.mention} ", view=view)

async def setup(bot): await bot.add_cog(GameRangeGuess(bot))