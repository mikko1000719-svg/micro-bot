import discord
from discord.ext import commands
from discord import app_commands

class RPSView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.choices = {player1: None, player2: None}

    async def handle_choice(self, interaction: discord.Interaction, choice: str):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("！", ephemeral=True)
            return
            
        if self.choices[interaction.user] is not None:
            await interaction.response.send_message("，！", ephemeral=True)
            return

        self.choices[interaction.user] = choice
        await interaction.response.send_message(f" {choice}！。", ephemeral=True)

        if self.choices[self.player1] and self.choices[self.player2]:
            await self.check_winner(interaction)

    async def check_winner(self, interaction: discord.Interaction):
        p1_choice = self.choices[self.player1]
        p2_choice = self.choices[self.player2]
        
        rules = {"✌️": "🖐️", "✊": "✌️", "🖐️": "✊"}
        
        result_text = f"**：**\n{self.player1.mention}  {p1_choice}\n{self.player2.mention}  {p2_choice}\n\n"
        
        if p1_choice == p2_choice:
            result_text += "[HANDSHAKE] **！**"
        elif rules[p1_choice] == p2_choice:
            result_text += f"[PARTY] ** {self.player1.mention} ！**"
        else:
            result_text += f"[PARTY] ** {self.player2.mention} ！**"

        for child in self.children:
            child.disabled = True
            
        await interaction.message.edit(content=result_text, view=self)

    @discord.ui.button(label="✌️", style=discord.ButtonStyle.primary)
    async def btn_scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "✌️")

    @discord.ui.button(label="✊", style=discord.ButtonStyle.primary)
    async def btn_rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "✊")

    @discord.ui.button(label="🖐️", style=discord.ButtonStyle.primary)
    async def btn_paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "🖐️")

class GameRPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_rps", description="！")
    async def play_rps(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("！", ephemeral=True)
            return
            
        view = RPSView(interaction.user, opponent)
        await interaction.response.send_message(f"[GAME] ****\n{interaction.user.mention} VS {opponent.mention}\n！", view=view)

async def setup(bot):
    await bot.add_cog(GameRPS(bot))