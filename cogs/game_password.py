import discord
import random
from discord.ext import commands
from discord import app_commands

class PasswordModal(discord.ui.Modal, title='Number'):
    number = discord.ui.TextInput(label='Number', style=discord.TextStyle.short)

    def __init__(self, view):
        super().__init__()
        self.game_view = view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            guess = int(self.number.value)
        except ValueError:
            await interaction.response.send_message("！", ephemeral=True)
            return

        await self.game_view.process_guess(interaction, guess)

class PasswordView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=180)
        self.player1 = player1
        self.player2 = player2
        self.current = player1
        self.target = random.randint(1, 100)
        self.min_val = 1
        self.max_val = 100

    @discord.ui.button(label="🔢 Number", style=discord.ButtonStyle.primary)
    async def guess_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current:
            await interaction.response.send_message("！", ephemeral=True)
            return
        await interaction.response.send_modal(PasswordModal(self))

    async def process_guess(self, interaction: discord.Interaction, guess: int):
        if guess <= self.min_val or guess >= self.max_val:
            await interaction.response.send_message(f" {self.min_val}  {self.max_val} Number！", ephemeral=True)
            return

        if guess == self.target:
            for child in self.children: child.disabled = True
            winner = self.player2 if self.current == self.player1 else self.player1
            msg = f"💥 **！** {self.current.mention} Number **{self.target}**！\n[PARTY]  {winner.mention} ！"
            await interaction.response.edit_message(content=msg, view=self)
        else:
            if guess > self.target: self.max_val = guess
            else: self.min_val = guess
            
            self.current = self.player2 if self.current == self.player1 else self.player1
            msg = f"🔢 ****\n：**{self.min_val} ~ {self.max_val}**\n {self.current.mention} Number！"
            await interaction.response.edit_message(content=msg, view=self)

class GamePassword(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_password", description=" (1-100)")
    async def play_password(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("！", ephemeral=True)
            return
        view = PasswordView(interaction.user, opponent)
        await interaction.response.send_message(f"🔢 ****\n：1 ~ 100\n {interaction.user.mention} ！", view=view)

async def setup(bot):
    await bot.add_cog(GamePassword(bot))