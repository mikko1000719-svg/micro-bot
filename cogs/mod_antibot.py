import discord
from discord.ext import commands
from discord import app_commands

class ModAntiBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 用來記錄哪些伺服器開啟了防 BOT 模式 (預設為 False)
        self.antibot_enabled = {}

    # 監聽成員加入事件
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # 如果加入的是機器人，且該伺服器開啟了防 BOT 模式
        if member.bot and self.antibot_enabled.get(member.guild.id, False):
            try:
                await member.kick(reason="Anti-Bot 系統已啟用，自動踢出未經授權的機器人")
            except Exception as e:
                print(f"防 BOT 踢出失敗: {e}")

    @app_commands.command(name="mod_antibot", description="開關防機器人模式，自動踢出新加入的 BOT")
    @app_commands.describe(enable="True 開啟保護 / False 關閉保護")
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_antibot(self, interaction: discord.Interaction, enable: bool):
        self.antibot_enabled[interaction.guild.id] = enable
        status = "🟢 已開啟" if enable else "🔴 已關閉"
        msg = f"🛡️ **防機器人 (Anti-Bot) 模式 {status}！**\n"
        if enable:
            msg += "系統將會自動踢出任何新加入伺服器的機器人。"
        
        await interaction.response.send_message(msg, ephemeral=True)

    @mod_antibot.error
    async def mod_antibot_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你需要「管理員」權限才能設定防 BOT 系統！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModAntiBot(bot))