import discord
import random
from discord.ext import commands
from discord import app_commands

class DrawView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.draws = {player1: None, player2: None}

    @discord.ui.button(label="🎋 ", style=discord.ButtonStyle.secondary)
    async def draw_stick(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("！", ephemeral=True)
            return
        if self.draws[interaction.user] is not None:
            await interaction.response.send_message("！", ephemeral=True)
            return

        luck = random.choice(["", "", "", ""])
        score_map = {"": 4, "": 3, "": 2, "": 1}
        self.draws[interaction.user] = (luck, score_map[luck])
        
        await interaction.response.send_message(f"【{luck}】！...", ephemeral=True)

        if self.draws[self.player1] is not None and self.draws[self.player2] is not None:
            button.disabled = True
            p1_l, p1_s = self.draws[self.player1]
            p2_l, p2_s = self.draws[self.player2]
            
            res = f"🎋 ****\n{self.player1.mention} ：{p1_l}\n{self.player2.mention} ：{p2_l}\n\n"
            if p1_s > p2_s: res += f"[PARTY]  {self.player1.mention} ！"
            elif p2_s > p1_s: res += f"[PARTY]  {self.player2.mention} ！"
            else: res += "[HANDSHAKE] ，！"

            await interaction.message.edit(content=res, view=self)

class GameDraw(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_draw", description="！")
    async def play_draw(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("！", ephemeral=True)
            return
        view = DrawView(interaction.user, opponent)
        await interaction.response.send_message(f"🎋 ****\n{interaction.user.mention} VS {opponent.mention}\n！", view=view)

async def setup(bot): await bot.add_cog(GameDraw(bot))