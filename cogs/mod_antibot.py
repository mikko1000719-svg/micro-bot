import discord
from discord.ext import commands
from discord import app_commands

# 建立自訂檢查器：確認使用者是否為伺服器擁有者
def is_guild_owner():
    def predicate(interaction: discord.Interaction) -> bool:
        # 確保在伺服器內執行，且使用者的 ID 等於伺服器擁有者的 ID
        return interaction.guild is not None and interaction.user.id == interaction.guild.owner_id
    return app_commands.check(predicate)

class ModAntiBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.antibot_enabled = {}

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot and self.antibot_enabled.get(member.guild.id, False):
            try:
                await member.kick(reason="Anti-Bot 系統已啟用，自動踢出未經授權的機器人")
            except Exception as e:
                print(f"防 BOT 踢出失敗: {e}")

    @app_commands.command(name="mod_antibot", description="開關防機器人模式，自動踢出新加入的 BOT")
    @app_commands.describe(enable="True 開啟保護 / False 關閉保護")
    @app_commands.default_permissions(administrator=True) # 對一般成員隱藏指令
    @is_guild_owner() # 核心：限制只有擁有者可以執行
    async def mod_antibot(self, interaction: discord.Interaction, enable: bool):
        self.antibot_enabled[interaction.guild.id] = enable
        status = "[OK] 已開啟" if enable else "[STOP] 已關閉"
        msg = f"[SHIELD] **防機器人 (Anti-Bot) 模式 {status}！**\n"
        if enable:
            msg += "系統將會自動踢出任何新加入伺服器的機器人。"
        
        await interaction.response.send_message(msg, ephemeral=True)

    @mod_antibot.error
    async def mod_antibot_error(self, interaction: discord.Interaction, error):
        # 攔截我們的自訂檢查錯誤
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message("[ERROR] 權限不足！此指令**僅限伺服器擁有者 (Owner)** 使用！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModAntiBot(bot))
