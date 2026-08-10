import discord
from discord import app_commands
from discord.ext import commands

class Passport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="passport", description="查看你的微國公民護照")
    async def passport(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        
        # 根據 User ID 產生專屬護照編號格式
        passport_no = f"PASSPORT-{user.id % 1000000:06d}"
        join_date = user.joined_at.strftime("%Y-%m-%d") if isinstance(user, discord.Member) and user.joined_at else "未知"

        embed = discord.Embed(
            title="🌐 微國聯邦官方護照 (Federal Passport)",
            description="本護照證明持有人為本微國之合法公民或入境貴賓。",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="公民姓名", value=f"**{user.display_name}**", inline=True)
        embed.add_field(name="護照編號", value=f"`{passport_no}`", inline=True)
        embed.add_field(name="所屬地區/伺服器", value=f"{guild.name if guild else '聯邦直轄區'}", inline=False)
        embed.add_field(name="簽發日期 (加入日)", value=f"`{join_date}`", inline=True)
        embed.add_field(name="身份狀態", value="✅ 驗證公民", inline=True)
        embed.set_footer(text="微國移民與邊境管理署 發行")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Passport(bot))