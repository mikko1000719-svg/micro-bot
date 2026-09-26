import discord
from discord.ext import commands
from discord import app_commands

class CmdEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="embed", description="將你輸入的文字轉為精美的 Embed 嵌入公告卡片")
    @app_commands.describe(title="公告標題", description="公告內文內容", color="顏色代碼 (可选，例如: red, blue, green)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def custom_embed(self, interaction: discord.Interaction, title: str, description: str, color: str = "blue"):
        # Convert顏色對應
        color_map = {
            "red": discord.Color.red(),
            "blue": discord.Color.blue(),
            "green": discord.Color.green(),
            "gold": discord.Color.gold(),
            "purple": discord.Color.purple(),
            "orange": discord.Color.orange()
        }
        embed_color = color_map.get(color.lower(), discord.Color.blue())
        
        embed = discord.Embed(title=title, description=description.replace("\\n", "\n"), color=embed_color)
        embed.set_footer(text=f"公告發布者：{interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("[OK] 嵌入公告已SuccessSend！", ephemeral=True)

    @custom_embed.error
    async def embed_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「ManageMessage」Permission才能發布 Embed 公告！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdEmbed(bot))