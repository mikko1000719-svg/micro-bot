import discord
from discord.ext import commands
from discord import app_commands

class ToolUserAvatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="useravatar", description="查看指定成員的高畫質大頭貼與下載連結")
    @app_commands.describe(member="要查看的成員 (留空則查看自己)")
    async def useravatar(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        avatar_url = target.display_avatar.url

        embed = discord.Embed(title=f"🖼️ {target.display_name} 的大頭貼", color=target.color)
        embed.set_image(url=avatar_url)
        embed.description = f"[點擊這裡直接開啟大頭貼原Graph]({avatar_url})"
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ToolUserAvatar(bot))