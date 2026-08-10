import discord
import random
from discord.ext import commands
from discord import app_commands

class PasswordModal(discord.ui.Modal, title='輸入你要猜的數字'):
    number = discord.ui.TextInput(label='請輸入數字', style=discord.TextStyle.short)

    def __init__(self, view):
        super().__init__()
        self.game_view = view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            guess = int(self.number.value)
        except ValueError:
            await interaction.response.send_message("請輸入整數喔！", ephemeral=True)
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

    @discord.ui.button(label="🔢 猜數字", style=discord.ButtonStyle.primary)
    async def guess_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current:
            await interaction.response.send_message("還沒輪到你！", ephemeral=True)
            return
        await interaction.response.send_modal(PasswordModal(self))

    async def process_guess(self, interaction: discord.Interaction, guess: int):
        if guess <= self.min_val or guess >= self.max_val:
            await interaction.response.send_message(f"請輸入 {self.min_val} 到 {self.max_val} 之間的數字！", ephemeral=True)
            return

        if guess == self.target:
            for child in self.children: child.disabled = True
            winner = self.player2 if self.current == self.player1 else self.player1
            msg = f"💥 **砰！** {self.current.mention} 踩到地雷數字 **{self.target}**！\n🎉 恭喜 {winner.mention} 獲勝！"
            await interaction.response.edit_message(content=msg, view=self)
        else:
            if guess > self.target: self.max_val = guess
            else: self.min_val = guess
            
            self.current = self.player2 if self.current == self.player1 else self.player1
            msg = f"🔢 **終極密碼**\n目前範圍：**{self.min_val} ~ {self.max_val}**\n輪到 {self.current.mention} 猜數字！"
            await interaction.response.edit_message(content=msg, view=self)

class GamePassword(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_password", description="與對手玩終極密碼 (1-100)")
    async def play_password(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = PasswordView(interaction.user, opponent)
        await interaction.response.send_message(f"🔢 **終極密碼開始**\n範圍：1 ~ 100\n由 {interaction.user.mention} 先猜！", view=view)

async def setup(bot):
    await bot.add_cog(GamePassword(bot))