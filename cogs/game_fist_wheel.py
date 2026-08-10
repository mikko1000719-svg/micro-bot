import discord
import random
from discord.ext import commands
from discord import app_commands

class FistWheelView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.results = {player1: None, player2: None}

    @discord.ui.button(label="✊ 轉動猜拳轉盤", style=discord.ButtonStyle.success)
    async def spin_fist(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的遊戲！", ephemeral=True)
            return
        if self.results[interaction.user] is not None:
            await interaction.response.send_message("你已經轉過轉盤了！", ephemeral=True)
            return

        moves = ["剪刀", "石頭", "布"]
        my_move = random.choice(moves)
        score_map = {"石頭": 3, "剪刀": 2, "布": 1}
        
        self.results[interaction.user] = (my_move, score_map[my_move])
        await interaction.response.send_message(f"轉盤結果：【{my_move}】！等待對手...", ephemeral=True)

        if self.results[self.player1] is not None and self.results[self.player2] is not None:
            button.disabled = True
            p1_move, p1_val = self.results[self.player1]
            p2_move, p2_val = self.results[self.player2]
            
            res = f"✊ **猜拳轉盤對決結算**\n{self.player1.mention} 轉出：{p1_move}\n{self.player2.mention} 轉出：{p2_move}\n\n"
            
            # 標準猜拳勝負判定
            if p1_move == p2_move:
                res += "🤝 雙方轉出相同拳形，平手！"
            elif (p1_move == "石頭" and p2_move == "剪刀") or \
                 (p1_move == "剪刀" and p2_move == "布") or \
                 (p1_move == "布" and p2_move == "石頭"):
                res += f"🎉 恭喜 {self.player1.mention} 獲勝！"
            else:
                res += f"🎉 恭喜 {self.player2.mention} 獲勝！"

            await interaction.message.edit(content=res, view=self)

class GameFistWheel(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_fistwheel", description="轉動猜拳轉盤進行對決！")
    async def play_fistwheel(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = FistWheelView(interaction.user, opponent)
        await interaction.response.send_message(f"✊ **猜拳轉盤對決開始**\n{interaction.user.mention} VS {opponent.mention}\n請雙方轉動轉盤！", view=view)

async def setup(bot): await bot.add_cog(GameFistWheel(bot))