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
            await interaction.response.send_message("這不是你的遊戲喔！", ephemeral=True)
            return
            
        if self.choices[interaction.user] is not None:
            await interaction.response.send_message("你已經出過拳了，請等待對手！", ephemeral=True)
            return

        self.choices[interaction.user] = choice
        await interaction.response.send_message(f"你出了 {choice}！請保密並等待對手。", ephemeral=True)

        if self.choices[self.player1] and self.choices[self.player2]:
            await self.check_winner(interaction)

    async def check_winner(self, interaction: discord.Interaction):
        p1_choice = self.choices[self.player1]
        p2_choice = self.choices[self.player2]
        
        rules = {"✌️剪刀": "🖐️布", "✊石頭": "✌️剪刀", "🖐️布": "✊石頭"}
        
        result_text = f"**結算結果：**\n{self.player1.mention} 出了 {p1_choice}\n{self.player2.mention} 出了 {p2_choice}\n\n"
        
        if p1_choice == p2_choice:
            result_text += "🤝 **平手！**"
        elif rules[p1_choice] == p2_choice:
            result_text += f"🎉 **恭喜 {self.player1.mention} 獲勝！**"
        else:
            result_text += f"🎉 **恭喜 {self.player2.mention} 獲勝！**"

        for child in self.children:
            child.disabled = True
            
        await interaction.message.edit(content=result_text, view=self)

    @discord.ui.button(label="✌️剪刀", style=discord.ButtonStyle.primary)
    async def btn_scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "✌️剪刀")

    @discord.ui.button(label="✊石頭", style=discord.ButtonStyle.primary)
    async def btn_rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "✊石頭")

    @discord.ui.button(label="🖐️布", style=discord.ButtonStyle.primary)
    async def btn_paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "🖐️布")

class GameRPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_rps", description="與另一位玩家對戰剪刀石頭布！")
    async def play_rps(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實的其他玩家！", ephemeral=True)
            return
            
        view = RPSView(interaction.user, opponent)
        await interaction.response.send_message(f"🎮 **剪刀石頭布**\n{interaction.user.mention} VS {opponent.mention}\n請雙方點擊下方按鈕出拳！", view=view)

async def setup(bot):
    await bot.add_cog(GameRPS(bot))