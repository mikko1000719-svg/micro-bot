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

    @discord.ui.button(label="🎋 抽取幸運籤", style=discord.ButtonStyle.secondary)
    async def draw_stick(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的遊戲！", ephemeral=True)
            return
        if self.draws[interaction.user] is not None:
            await interaction.response.send_message("你已經抽過籤了！", ephemeral=True)
            return

        luck = random.choice(["大吉", "中吉", "小吉", "凶"])
        score_map = {"大吉": 4, "中吉": 3, "小吉": 2, "凶": 1}
        self.draws[interaction.user] = (luck, score_map[luck])
        
        await interaction.response.send_message(f"你抽到了【{luck}】！等待對手...", ephemeral=True)

        if self.draws[self.player1] is not None and self.draws[self.player2] is not None:
            button.disabled = True
            p1_l, p1_s = self.draws[self.player1]
            p2_l, p2_s = self.draws[self.player2]
            
            res = f"🎋 **抽籤對決結算**\n{self.player1.mention} 抽到：{p1_l}\n{self.player2.mention} 抽到：{p2_l}\n\n"
            if p1_s > p2_s: res += f"🎉 恭喜 {self.player1.mention} 運氣較好獲勝！"
            elif p2_s > p1_s: res += f"🎉 恭喜 {self.player2.mention} 運氣較好獲勝！"
            else: res += "🤝 雙方抽到同等級的籤，平手！"

            await interaction.message.edit(content=res, view=self)

class GameDraw(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_draw", description="抽取幸運籤比拼運氣！")
    async def play_draw(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = DrawView(interaction.user, opponent)
        await interaction.response.send_message(f"🎋 **幸運抽籤對決**\n{interaction.user.mention} VS {opponent.mention}\n請雙方抽取幸運籤！", view=view)

async def setup(bot): await bot.add_cog(GameDraw(bot))