import discord
import random
from discord.ext import commands
from discord import app_commands

class CardDuelView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.cards = {player1: None, player2: None}

    @discord.ui.button(label=" ", style=discord.ButtonStyle.secondary)
    async def draw_card(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("", ephemeral=True)
            return
        if self.cards[interaction.user] is not None:
            await interaction.response.send_message("", ephemeral=True)
            return

        card_val = random.randint(1, 13)
        self.cards[interaction.user] = card_val
        await interaction.response.send_message(f" {card_val} ...", ephemeral=True)

        if self.cards[self.player1] is not None and self.cards[self.player2] is not None:
            button.disabled = True
            p1_c = self.cards[self.player1]
            p2_c = self.cards[self.player2]
            
            res = f" ****\n{self.player1.mention} **{p1_c}**\n{self.player2.mention} **{p2_c}**\n\n"
            if p1_c > p2_c: res += f"[TROPHY]  {self.player1.mention} "
            elif p2_c > p1_c: res += f"[TROPHY]  {self.player2.mention} "
            else: res += "[HANDSHAKE] "

            await interaction.message.edit(content=res, view=self)

class GameCardDuel(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_cardduel", description="指令說明")
    async def play_cardduel(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
        view = CardDuelView(interaction.user, opponent)
        await interaction.response.send_message(f" ****\n{interaction.user.mention} VS {opponent.mention}\n", view=view)

async def setup(bot): await bot.add_cog(GameCardDuel(bot))