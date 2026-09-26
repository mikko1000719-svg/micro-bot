import discord
from discord.ext import commands
from discord import app_commands

# 建立自訂檢查器：確認使用者是否為伺服器擁有者
def is_guild_owner():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.guild is not None and interaction.user.id == interaction.guild.owner_id
    return app_commands.check(predicate)

class ModNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_nuke", description="核彈級清頻：重建目前頻道並刪除舊頻道（無法復原）")
    @app_commands.default_permissions(administrator=True) # 對一般成員隱藏指令
    @is_guild_owner() # 核心：限制只有擁有者可以執行
    async def mod_nuke(self, interaction: discord.Interaction):
        channel = interaction.channel
        
        await interaction.response.send_message("準備發射核彈，頻道即將重建...", ephemeral=True)
        
        try:
            new_channel = await channel.clone(reason=f"由擁有者 {interaction.user} 使用 nuke 指令重建")
            await new_channel.edit(position=channel.position)
            
            await channel.delete(reason="核彈清頻刪除舊頻道")
            
            await new_channel.send(f"💥 轟！本頻道已被擁有者 {interaction.user.mention} 重新建立，所有舊訊息已清理完畢。")
        except Exception as e:
            print(f"Nuke 失敗: {e}")

    @mod_nuke.error
    async def mod_nuke_error(self, interaction: discord.Interaction, error):
        # 攔截我們的自訂檢查錯誤
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message("[ERROR] 權限不足！此指令**僅限伺服器擁有者 (Owner)** 使用！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModNuke(bot))
