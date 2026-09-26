import discord
from discord.ext import commands
from discord import app_commands

# 建立CustomCheck器：Confirm使用者是否為Server擁有者
def is_guild_owner():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.guild is not None and interaction.user.id == interaction.guild.owner_id
    return app_commands.check(predicate)

class ModNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_nuke", description="核彈級清頻：重建目前Channel並Delete舊Channel（無法復原）")
    @app_commands.default_permissions(administrator=True) # 對一般成員HiddenCommand
    @is_guild_owner() # 核心：Limit只有擁有者可以Execute
    async def mod_nuke(self, interaction: discord.Interaction):
        channel = interaction.channel
        
        await interaction.response.send_message("準備發射核彈，Channel即將重建...", ephemeral=True)
        
        try:
            new_channel = await channel.clone(reason=f"由擁有者 {interaction.user} 使用 nuke Command重建")
            await new_channel.edit(position=channel.position)
            
            await channel.delete(reason="核彈清頻Delete舊Channel")
            
            await new_channel.send(f"💥 轟！本Channel已被擁有者 {interaction.user.mention} Re-建立，所有舊Message已清理完畢。")
        except Exception as e:
            print(f"Nuke Failed: {e}")

    @mod_nuke.error
    async def mod_nuke_error(self, interaction: discord.Interaction, error):
        # 攔截我們的CustomCheckError
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message("[ERROR] Permission不足！此Command**僅限Server擁有者 (Owner)** 使用！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModNuke(bot))
