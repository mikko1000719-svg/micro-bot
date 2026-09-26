import discord
from discord.ext import commands
from discord import app_commands

class Broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 儲存拒收通知的使用者 ID 集合
        self.opt_out_users = set()

    @app_commands.command(name="optout", description="[微國 5.0] 切換是否拒收機器人的全體私訊廣播通知")
    async def optout(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.opt_out_users:
            self.opt_out_users.remove(user_id)
            await interaction.response.send_message("[OK] 您已**取消**拒收通知，未來將可正常接收微國廣播。", ephemeral=True)
        else:
            self.opt_out_users.add(user_id)
            await interaction.response.send_message("🔕 您已成功加入**拒收清單**，將不再接收機器人的全體私訊廣播。", ephemeral=True)

    @app_commands.command(name="broadcast", description="[微國 5.0] 發送私訊廣播給伺服器全體成員（自動略過拒收者）")
    @app_commands.describe(message="要廣播的公告內容")
    @app_commands.checks.has_permissions(administrator=True)
    async def broadcast(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        success_count = 0
        skip_count = 0

        embed = discord.Embed(
            title="[SPEAKER] 【微國機器人 5.0】全體公告廣播",
            description=message,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"來自伺服器：{guild.name}")

        for member in guild.members:
            if member.bot:
                continue
            if member.id in self.opt_out_users:
                skip_count += 1
                continue
            
            try:
                await member.send(embed=embed)
                success_count += 1
            except Exception:
                # 使用者可能關閉了私訊功能
                skip_count += 1

        await interaction.followup.send(
            f"[OK] 廣播發送完畢！\n- 成功發送人數：**{success_count}**\n- 略過/未送達人數：**{skip_count}**", 
            ephemeral=True
        )

    @broadcast.error
    async def broadcast_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 權限不足！只有管理員可以執行全體廣播。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Broadcast(bot))