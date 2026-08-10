import discord
from discord.ext import commands
from discord import app_commands

class ModCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_check", description="檢查指定成員在目前頻道的基礎發言與連結權限")
    @app_commands.describe(member="要檢查的成員")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mod_check(self, interaction: discord.Interaction, member: discord.Member):
        channel = interaction.channel
        permissions = channel.permissions_for(member)
        
        embed = discord.Embed(title=f"🛡️ 成員權限檢查：{member.display_name}", color=discord.Color.blue())
        embed.add_field(name="可以發送訊息", value="✅ 是" if permissions.send_messages else "❌ 否", inline=True)
        embed.add_field(name="可以嵌入連結", value="✅ 是" if permissions.embed_links else "❌ 否", inline=True)
        embed.add_field(name="可以附加檔案", value="✅ 是" if permissions.attach_files else "❌ 否", inline=True)
        embed.add_field(name="可以新增表情符號", value="✅ 是" if permissions.add_reactions else "❌ 否", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @mod_check.error
    async def mod_check_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有權限使用此指令！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModCheck(bot))