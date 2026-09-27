import discord
from discord.ext import commands
from discord import app_commands

class UtilityTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. CommandGroup (Group)
    # name="utility" CommandDiscord  1 Command
    utility_group = app_commands.Group(name="utility", description="CommandGroup")

    # 2. CommandGroup
    #  @app_commands.command  @utility_group.command
    @utility_group.command(name="ping", description="Command description")
    async def ping_command(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f" {latency}ms")

    @utility_group.command(name="dice", description="Command description")
    async def dice_command(self, interaction: discord.Interaction):
        import random
        result = random.randint(1, 6)
        await interaction.response.send_message(f"🎲 {result}")

    # (Continue @utility_group.command  20 Command...)

async def setup(bot):
    await bot.add_cog(UtilityTools(bot))