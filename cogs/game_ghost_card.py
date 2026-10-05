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

    @discord.ui.button(label=" ", style=discord.ButtonStyle.danger)
    async def draw_ghost(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.current:
            await interaction.response.send_message("", ephemeral=True)
            return

        if self.step == self.ghost_slot:
            for child in self.children: child.disabled = True
            loser = self.current
            winner = self.player2 if loser == self.player1 else self.player1
            msg = f" **** {loser.mention} \n🎉  {winner.mention} "
            await interaction.response.edit_message(content=msg, view=self)
        else:
            self.step += 1
            self.current = self.player2 if self.current == self.player1 else self.player1
            msg = f" ****\nSecuritySecurity\n {self.current.mention} "
            await interaction.response.edit_message(content=msg, view=self)

class GameGhostCard(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_ghostcard", description="指令說明")
    async def play_ghostcard(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
        view = GhostCardView(interaction.user, opponent)
        await interaction.response.send_message(f" ****\n{interaction.user.mention} VS {opponent.mention}\n {interaction.user.mention} ", view=view)

async def setup(bot): await bot.add_cog(GameGhostCard(bot))