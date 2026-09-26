import discord
from discord import app_commands
from discord.ext import commands

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Send官方公告至指定Channel")
    @app_commands.checks.has_permissions(administrator=True)
    async def announce(
        self, 
        interaction: discord.Interaction, 
        channel: discord.TextChannel, 
        title: str, 
        content: str
    ):
        """
        channel: 選擇要Send公告的Channel
        title: 公告標題
        content: 公告內容 (支援 \n 換行)
        """
        # 換行符號Process
        formatted_content = content.replace("\\n", "\n")

        embed = discord.Embed(
            title=f"[SPEAKER] {title}",
            description=formatted_content,
            color=discord.Color.red()
        )
        embed.set_footer(text=f"發布者: {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        try:
            await channel.send(embed=embed)
            await interaction.response.send_message(f"[OK] 公告已SuccessSend至 {channel.mention}！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 公告SendFailed，原因: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announce(bot))