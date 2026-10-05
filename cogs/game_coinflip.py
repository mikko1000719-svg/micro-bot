import discord
import random
from discord.ext import commands
from discord import app_commands

class CoinFlipView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.choices = {player1: None, player2: None}

    async def make_choice(self, interaction: discord.Interaction, choice: str):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("", ephemeral=True)
            return
        if self.choices[interaction.user] is not None:
            await interaction.response.send_message("", ephemeral=True)
            return

        self.choices[interaction.user] = choice
        await interaction.response.send_message(f"{choice}...", ephemeral=True)

        if self.choices[self.player1] and self.choices[self.player2]:
            result = random.choice(["", ""])
            res_msg = f"🪙 **{result}**\n\n"
            res_msg += f"{self.player1.mention}  {self.choices[self.player1]}\n"
            res_msg += f"{self.player2.mention}  {self.choices[self.player2]}\n\n"

            winner = None
            if self.choices[self.player1] == result:
                winner = self.player1
            elif self.choices[self.player2] == result:
                winner = self.player2

            if winner:
                res_msg += f"🎉  {winner.mention} "
            else:
                res_msg += "[HANDSHAKE] "

            for child in self.children: child.disabled = True
            await interaction.message.edit(content=res_msg, view=self)

    @discord.ui.button(label="🪙 ", style=discord.ButtonStyle.primary)
    async def heads(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "")

    @discord.ui.button(label="🪙 ", style=discord.ButtonStyle.danger)
    async def tails(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "")

class GameCoinFlip(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_coinflip", description="指令說明")
    async def play_coinflip(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
        view = CoinFlipView(interaction.user, opponent)
        await interaction.response.send_message(f"🪙 ****\n{interaction.user.mention} VS {opponent.mention}\n", view=view)

async def setup(bot): await bot.add_cog(GameCoinFlip(bot))