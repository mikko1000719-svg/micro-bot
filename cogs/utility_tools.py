import discord
from discord.ext import commands
from discord import app_commands

class UtilityTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. 建立一個CommandGroup (Group)
    # name="utility" 代表最上層的Command名稱，Discord 只會把這個算作 1 個Command配額
    utility_group = app_commands.Group(name="utility", description="實用工具包CommandGroup")

    # 2. 將原本的Command綁定到這個Group底下
    # 注意：這裡的裝飾器從 @app_commands.command 變成了 @utility_group.command
    @utility_group.command(name="ping", description="查看Bot的延遲時間")
    async def ping_command(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 延遲：{latency}ms")

    @utility_group.command(name="dice", description="擲骰子工具")
    async def dice_command(self, interaction: discord.Interaction):
        import random
        result = random.randint(1, 6)
        await interaction.response.send_message(f"[DICE] 你擲出了：{result}")

    # (你可以Continue用 @utility_group.command 把剩下的 20 幾個Command都加進來...)

async def setup(bot):
    await bot.add_cog(UtilityTools(bot))