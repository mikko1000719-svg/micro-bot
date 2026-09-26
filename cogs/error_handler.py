# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord import app_commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        # 紀錄錯誤訊息至 OwnerDM 模組
        owner_cog = self.bot.get_cog("OwnerDM")
        if owner_cog:
            owner_cog.log_error(str(error))

        if isinstance(error, app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(f"[TIME] Command on cooldown, please wait {round(error.retry_after, 1)} seconds.", ephemeral=True)
        elif isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] You don't have permission to execute this command!", ephemeral=True)
        else:
            print(f"[AppCommand Error] {error}")

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
