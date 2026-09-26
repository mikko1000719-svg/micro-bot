import discord
import random
from discord.ext import commands
from discord import app_commands

class CoinFlipView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.choices = {player1: None, player2: None}

    async def make_choice(self, interaction: discord.Interaction, choice: str):
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("這不是你的遊戲！", ephemeral=True)
            return
        if self.choices[interaction.user] is not None:
            await interaction.response.send_message("你已經選過了！", ephemeral=True)
            return

        self.choices[interaction.user] = choice
        await interaction.response.send_message(f"你選擇了【{choice}】！等待對手選擇...", ephemeral=True)

        if self.choices[self.player1] and self.choices[self.player2]:
            result = random.choice(["正面", "反面"])
            res_msg = f"🪙 **硬幣結果：{result}**\n\n"
            res_msg += f"{self.player1.mention} 選擇 {self.choices[self.player1]}\n"
            res_msg += f"{self.player2.mention} 選擇 {self.choices[self.player2]}\n\n"

            winner = None
            if self.choices[self.player1] == result:
                winner = self.player1
            elif self.choices[self.player2] == result:
                winner = self.player2

            if winner:
                res_msg += f"[PARTY] 恭喜 {winner.mention} 猜中獲勝！"
            else:
                res_msg += "[HANDSHAKE] 雙方都沒猜中，平手！"

            for child in self.children: child.disabled = True
            await interaction.message.edit(content=res_msg, view=self)

    @discord.ui.button(label="🪙 正面", style=discord.ButtonStyle.primary)
    async def heads(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "正面")

    @discord.ui.button(label="🪙 反面", style=discord.ButtonStyle.danger)
    async def tails(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "反面")

class GameCoinFlip(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="play_coinflip", description="與對手進行硬幣正反面猜測對決！")
    async def play_coinflip(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot or opponent == interaction.user:
            await interaction.response.send_message("請標記一位真實玩家！", ephemeral=True)
            return
        view = CoinFlipView(interaction.user, opponent)
        await interaction.response.send_message(f"🪙 **硬幣猜測對決**\n{interaction.user.mention} VS {opponent.mention}\n請雙方選擇正面或反面！", view=view)

async def setup(bot): await bot.add_cog(GameCoinFlip(bot))