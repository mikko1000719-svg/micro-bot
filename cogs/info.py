import discord
from discord import app_commands
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="查看目前Server的詳細Information")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("此Command只能在Server中使用！", ephemeral=True)
            return

        # 建立漂亮的 Embed 卡片
        embed = discord.Embed(
            title=f"🏰 {guild.name} ServerInformation",
            color=discord.Color.blue()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="擁有者", value=f"{guild.owner.mention if guild.owner else '未知'}", inline=True)
        embed.add_field(name="總成員數", value=f"{guild.member_count} 人", inline=True)
        embed.add_field(name="文字Channel數", value=f"{len(guild.text_channels)} 個", inline=True)
        embed.add_field(name="語音Channel數", value=f"{len(guild.voice_channels)} 個", inline=True)
        embed.add_field(name="建立時間", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))