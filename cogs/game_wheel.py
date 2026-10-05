import discord
import random
from discord.ext import commands
from discord import app_commands

class WheelView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.spins = {player1: None, player2: None}

    @discord.ui.button(label=" ", style=discord.ButtonStyle.success)
    async def spin_wheel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("", ephemeral=True)
            return
        if self.spins[interaction.user] is not None:
            await interaction.response.send_message("", ephemeral=True)
            return

        score = random.randint(10, 100)
        self.spins[interaction.user] = score
        await interaction.response.send_message(f" **{score}** ...", ephemeral=True)

        if self.spins[self.player1] is not None and self.spins[self.player2] is not None:
            button.disabled = True
            p1_s = self.spins[self.player1]
            p2_s = self.spins[self.player2]
            
            res = f" ****\n{self.player1.mention} **{p1_s}**\n{self.player2.mention} **{p2_s}**\n\n"
            if p1_s > p2_s: res += f"[TROPHY]  {self.player1.mention} "
            elif p2_s > p1_s: res += f"[TROPHY]  {self.player2.mention} "
            else: res += "[HANDSHAKE] "

            await interaction.message.edit(content=res, view=self)

class GameWheel(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_wheel", description="指令說明")
    async def play_wheel(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
        view = WheelView(interaction.user, opponent)
        await interaction.response.send_message(f" ****\n{interaction.user.mention} VS {opponent.mention}\n", view=view)

async def setup(bot): await bot.add_cog(GameWheel(bot))