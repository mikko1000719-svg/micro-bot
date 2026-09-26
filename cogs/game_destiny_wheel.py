import discord
import random
from discord.ext import commands
from discord import app_commands

class DestinyWheelView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.points = {player1: None, player2: None}

    @discord.ui.button(label="🎡 ", style=discord.ButtonStyle.primary)
    async def spin_destiny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("！", ephemeral=True)
            return
        if self.points[interaction.user] is not None:
            await interaction.response.send_message("！", ephemeral=True)
            return

        pt = random.randint(1, 1000)
        self.points[interaction.user] = pt
        await interaction.response.send_message(f"：**{pt}** ！...", ephemeral=True)

        if self.points[self.player1] is not None and self.points[self.player2] is not None:
            button.disabled = True
            p1_p = self.points[self.player1]
            p2_p = self.points[self.player2]
            
            res = f"🎡 ****\n{self.player1.mention} ：**{p1_p}** \n{self.player2.mention} ：**{p2_p}** \n\n"
            if p1_p > p2_p: res += f"[PARTY]  {self.player1.mention} ！"
            elif p2_p > p1_p: res += f"[PARTY]  {self.player2.mention} ！"
            else: res += "[HANDSHAKE] ，！"

            await interaction.message.edit(content=res, view=self)

class GameDestinyWheel(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_destinywheel", description="！")
    async def play_destinywheel(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("！", ephemeral=True)
            return
        view = DestinyWheelView(interaction.user, opponent)
        await interaction.response.send_message(f"🎡 ****\n{interaction.user.mention} VS {opponent.mention}\n！", view=view)

async def setup(bot): await bot.add_cog(GameDestinyWheel(bot))