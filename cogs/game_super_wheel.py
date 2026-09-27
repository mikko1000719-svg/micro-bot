import discord
import random
from discord.ext import commands
from discord import app_commands

class SuperWheelView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.results = {player1: None, player2: None}

    @discord.ui.button(label="⭐ Start", style=discord.ButtonStyle.primary)
    async def spin(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("", ephemeral=True)
            return
        if self.results[interaction.user] is not None:
            await interaction.response.send_message("", ephemeral=True)
            return

        val = random.randint(50, 500)
        self.results[interaction.user] = val
        await interaction.response.send_message(f"**{val}** ...", ephemeral=True)

        if self.results[self.player1] is not None and self.results[self.player2] is not None:
            button.disabled = True
            p1_v = self.results[self.player1]
            p2_v = self.results[self.player2]
            
            res = f"⭐ ****\n{self.player1.mention} **{p1_v}** \n{self.player2.mention} **{p2_v}** \n\n"
            if p1_v > p2_v: res += f"🎉  {self.player1.mention} "
            elif p2_v > p1_v: res += f"🎉  {self.player2.mention} "
            else: res += "[HANDSHAKE] "

            await interaction.message.edit(content=res, view=self)

class GameSuperWheel(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_superwheel", description="Start")
    async def play_superwheel(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
        view = SuperWheelView(interaction.user, opponent)
        await interaction.response.send_message(f"⭐ ****\n{interaction.user.mention} VS {opponent.mention}\nStart", view=view)

async def setup(bot): await bot.add_cog(GameSuperWheel(bot))