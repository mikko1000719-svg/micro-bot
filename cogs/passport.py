import discord
from discord import app_commands
from discord.ext import commands

class Passport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="passport", description="指令說明")
    async def passport(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        
        #  User ID Format
        passport_no = f"PASSPORT-{user.id % 1000000:06d}"
        join_date = user.joined_at.strftime("%Y-%m-%d") if isinstance(user, discord.Member) and user.joined_at else ""

        embed = discord.Embed(
            title="🌐  (Federal Passport)",
            description="指令說明",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Parameter description", value=f"**{user.display_name}**", inline=True)
        embed.add_field(name="Parameter description", value=f"`{passport_no}`", inline=True)
        embed.add_field(name="/Server", value=f"{guild.name if guild else ''}", inline=False)
        embed.add_field(name=" ()", value=f"`{join_date}`", inline=True)
        embed.add_field(name="Parameter description", value="✅ Verify", inline=True)
        embed.set_footer(text="EdgeManage ")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Passport(bot))