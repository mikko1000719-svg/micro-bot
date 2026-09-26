import discord
from discord.ext import commands
from discord import app_commands

class CmdClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="快速清除頻道中的指定數量歷史訊息")
    @app_commands.describe(amount="要清除的訊息數量 (1 到 100 條)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("[ERROR] 一次只能清除 1 到 100 條訊息！", ephemeral=True)
            return
            
        # 先回覆使用者避免 interaction逾時
        await interaction.response.defer(ephemeral=True)
        
        # 執行批次刪除
        deleted = await interaction.channel.purge(limit=amount)
        
        await interaction.followup.send(f"🧹 成功清除了 **{len(deleted)}** 條訊息！", ephemeral=True)

    @clear.error
    async def clear_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「管理訊息」權限才能清除訊息！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdClear(bot))