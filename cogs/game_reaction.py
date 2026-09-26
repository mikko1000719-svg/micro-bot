import discord
import asyncio
import random
from discord.ext import commands
from discord import app_commands

class ReactionView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=60)
        self.players = [player1, player2]
        self.clicked = False

    @discord.ui.button(label="[BOLT] ", style=discord.ButtonStyle.danger)
    async def click_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            await interaction.response.send_message("", ephemeral=True)
            return
            
        if not self.clicked:
            self.clicked = True
            button.disabled = True
            button.style = discord.ButtonStyle.success
            await interaction.response.edit_message(content=f"[PARTY] \n[BOLT] **{interaction.user.mention}** ", view=self)

class GameReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_reaction", description="")
    async def play_reaction(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("", ephemeral=True)
            return

        await interaction.response.send_message(f"[BOLT] {interaction.user.mention} VS {opponent.mention}\n**...** ()")
        
        #  2  6 
        await asyncio.sleep(random.uniform(2.0, 6.0))
        
        view = ReactionView(interaction.user, opponent)
        # SendMessageUpdate
        msg = await interaction.original_response()
        await msg.edit(content=f" ****\n{interaction.user.mention} VS {opponent.mention}", view=view)

async def setup(bot):
    await bot.add_cog(GameReaction(bot))