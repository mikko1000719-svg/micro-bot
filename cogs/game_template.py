import discord
import random
from discord.ext import commands
from discord import app_commands

class TemplateView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.ready = {player1: False, player2: False}

    @discord.ui.button(label="🎲 ", style=discord.ButtonStyle.primary)
    async def action_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            return
            
        self.ready[interaction.user] = True
        
        if self.ready[self.player1] and self.ready[self.player2]:
            button.disabled = True
            
            # --- Custom ---
            p1_score = random.randint(1, 10)
            p2_score = random.randint(1, 10)
            
            res = f"\n{self.player1.mention}  {p1_score}\n{self.player2.mention}  {p2_score}\n\n"
            if p1_score > p2_score: res += f"[TROPHY] {self.player1.mention} "
            elif p2_score > p1_score: res += f"[TROPHY] {self.player2.mention} "
            else: res += "[HANDSHAKE] "
            # -------------------------------
            
            await interaction.response.edit_message(content=res, view=self)
        else:
            await interaction.response.edit_message(content=f"✅ {interaction.user.mention} ...")

class GameTemplate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_custom", description="自定義")
    async def play_custom(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return
        view = TemplateView(interaction.user, opponent)
        await interaction.response.send_message(f" **Custom**\n{interaction.user.mention} VS {opponent.mention}\n", view=view)

async def setup(bot):
    await bot.add_cog(GameTemplate(bot))