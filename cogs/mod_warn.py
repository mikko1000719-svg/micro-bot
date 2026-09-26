import discord
from discord.ext import commands
from discord import app_commands

class ModWarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_warn", description="向指定成員Send正式Warning通知")
    @app_commands.describe(member="要Warning的成員", reason="Warning的原因")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            embed = discord.Embed(title="[WARNING] ServerWarning通知", color=discord.Color.orange())
            embed.description = f"您在Server **{interaction.guild.name}** 收到了Manage員的Warning。"
            embed.add_field(name="原因", value=reason)
            await member.send(embed=embed)
            dm_status = "[OK] 已Success私訊通知該成員。"
        except discord.Forbidden:
            dm_status = "[WARNING] 無法私訊該成員（可能關閉了私訊Function）。"

        await interaction.response.send_message(f"🚨 已對 {member.mention} 記錄Warning。\n**原因**：{reason}\n{dm_status}")

    @mod_warn.error
    async def mod_warn_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「Manage員」Permission才能使用此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModWarn(bot))
