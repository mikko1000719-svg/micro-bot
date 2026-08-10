import discord
from discord.ext import commands
from discord import app_commands

class ModNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_nuke", description="核彈級清頻：重建目前頻道並刪除舊頻道（無法復原）")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def mod_nuke(self, interaction: discord.Interaction):
        channel = interaction.channel
        
        # 先回覆 interaction，避免報錯
        await interaction.response.send_message("準備發射核彈，頻道即將重建...", ephemeral=True)
        
        try:
            # 複製一個設定一模一樣的新頻道，並放在原本的排序位置
            new_channel = await channel.clone(reason=f"由 {interaction.user} 使用 nuke 指令重建")
            await new_channel.edit(position=channel.position)
            
            # 刪除舊頻道
            await channel.delete(reason="核彈清頻刪除舊頻道")
            
            # 在新頻道發送成功訊息
            await new_channel.send(f"💥 轟！本頻道已被 {interaction.user.mention} 重新建立，所有舊訊息已清理完畢。")
        except Exception as e:
            print(f"Nuke 失敗: {e}")

    @mod_nuke.error
    async def mod_nuke_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 你沒有「管理頻道」的權限！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModNuke(bot))