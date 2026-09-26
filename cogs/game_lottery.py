import discord
import random
from discord.ext import commands
from discord import app_commands

class LotteryView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.tickets = {player1: None, player2: None}

    @discord.ui.button(label=" ", style=discord.ButtonStyle.success)
    async def buy_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("", ephemeral=True)
            return
        if self.tickets[interaction.user] is not None:
            await interaction.response.send_message("", ephemeral=True)
            return

        num = random.randint(1000, 9999)
        self.tickets[interaction.user] = num
        await interaction.response.send_message(f"**{num}**...", ephemeral=True)

        if self.tickets[self.player1] is not None and self.tickets[self.player2] is not None:
            button.disabled = True
            p1_n = self.tickets[self.player1]
            p2_n = self.tickets[self.player2]
            
            res = f" ****\n{self.player1.mention} **{p1_n}**\n{self.player2.mention} **{p2_n}**\n\n"
            if p1_n > p2_n: res += f"[TROPHY]  {self.player1.mention} "
            elif p2_n > p1_n: res += f"[TROPHY]  {self.player2.mention} "
            else: res += "[HANDSHAKE] "

            await interaction.message.edit(content=res, view=self)

class GameLottery(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_lottery", description="")
    async def play_lottery(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
        view = LotteryView(interaction.user, opponent)
        await interaction.response.send_message(f" ****\n{interaction.user.mention} VS {opponent.mention}\n", view=view)

async def setup(bot): await bot.add_cog(GameLottery(bot))