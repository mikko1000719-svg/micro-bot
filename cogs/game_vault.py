import discord
import random
from discord.ext import commands
from discord import app_commands

class VaultView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.current = player1
        self.vault_code = random.randint(100, 999)
        self.attempts = 0

    @discord.ui.button(label="[UNLOCK]  (100-999)", style=discord.ButtonStyle.success)
    async def try_vault(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current:
            await interaction.response.send_message("！", ephemeral=True)
            return

        # 
        hit = random.random() < 0.25 # 25% 
        if hit or self.attempts >= 5:
            for child in self.children: child.disabled = True
            winner = self.current
            msg = f"💥 **！** {winner.mention} Success（：{self.vault_code}）！\n[PARTY] ，！"
            await interaction.response.edit_message(content=msg, view=self)
        else:
            self.attempts += 1
            self.current = self.player2 if self.current == self.player1 else self.player1
            msg = f"[LOCKED2] ****\n {self.attempts} Failed，Defense...\n {self.current.mention} ！"
            await interaction.response.edit_message(content=msg, view=self)

class GameVault(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_vault", description="！")
    async def play_vault(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("！", ephemeral=True)
            return
        view = VaultView(interaction.user, opponent)
        await interaction.response.send_message(f"[LOCKED2] ****\n{interaction.user.mention} VS {opponent.mention}\n {interaction.user.mention} ！", view=view)

async def setup(bot): await bot.add_cog(GameVault(bot))