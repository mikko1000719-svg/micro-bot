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

    @discord.ui.button(label="🎲 擲骰子 (1-100)", style=discord.ButtonStyle.success)
    async def roll_dice(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的遊戲喔！", ephemeral=True)
            return
            
        if self.scores[interaction.user] is not None:
            await interaction.response.send_message("你已經擲過骰子了！", ephemeral=True)
            return

        roll = random.randint(1, 100)
        self.scores[interaction.user] = roll
        
        if self.scores[self.player1] is not None and self.scores[self.player2] is not None:
            button.disabled = True
            p1_score = self.scores[self.player1]
            p2_score = self.scores[self.player2]
            
            result_msg = f"🎲 **擲骰結果：**\n{self.player1.mention} 擲出了 **{p1_score}** 點！\n{self.player2.mention} 擲出了 **{p2_score}** 點！\n\n"
            
            if p1_score > p2_score:
                result_msg += f"🎉 {self.player1.mention} 獲勝！"
            elif p2_score > p1_score:
                result_msg += f"🎉 {self.player2.mention} 獲勝！"
            else:
                result_msg += "🤝 雙方平手！"
                
            await interaction.response.edit_message(content=result_msg, view=self)
        else:
            await interaction.response.edit_message(content=f"🎲 {interaction.user.mention} 已經擲出骰子！等待對手...")

class GameDice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play_dice", description="與另一位玩家比大小 (1-100)！")
    async def play_dice(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實的其他玩家！", ephemeral=True)
            return
            
        view = DiceView(interaction.user, opponent)
        await interaction.response.send_message(f"🎲 **擲骰子比大小**\n{interaction.user.mention} VS {opponent.mention}\n請雙方點擊下方按鈕擲出骰子！", view=view)

async def setup(bot):
    await bot.add_cog(GameDice(bot))