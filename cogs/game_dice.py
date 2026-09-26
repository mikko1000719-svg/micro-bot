import discord
import random
from discord.ext import commands
from discord import app_commands

class DiceView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.scores = {player1: None, player2: None}

    @discord.ui.button(label="[DICE]  (1-100)", style=discord.ButtonStyle.success)
    async def roll_dice(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("", ephemeral=True)
            return
            
        if self.scores[interaction.user] is not None:
            await interaction.response.send_message("", ephemeral=True)
            return

        roll = random.randint(1, 100)
        self.scores[interaction.user] = roll
        
        if self.scores[self.player1] is not None and self.scores[self.player2] is not None:
            button.disabled = True
            p1_score = self.scores[self.player1]
            p2_score = self.scores[self.player2]
            
            result_msg = f"[DICE] ****\n{self.player1.mention}  **{p1_score}** \n{self.player2.mention}  **{p2_score}** \n\n"
            
            if p1_score > p2_score:
                result_msg += f"[PARTY] {self.player1.mention} "
            elif p2_score > p1_score:
                result_msg += f"[PARTY] {self.player2.mention} "
            else:
                result_msg += "[HANDSHAKE] "
                
            await interaction.response.edit_message(content=result_msg, view=self)
        else:
            await interaction.response.edit_message(content=f"[DICE] {interaction.user.mention} ...")

class GameDice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_dice", description=" (1-100)")
    async def play_dice(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
            
        view = DiceView(interaction.user, opponent)
        await interaction.response.send_message(f"[DICE] ****\n{interaction.user.mention} VS {opponent.mention}\n", view=view)

async def setup(bot):
    await bot.add_cog(GameDice(bot))