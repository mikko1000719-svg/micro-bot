import discord
from discord import app_commands
from discord.ext import commands

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="建立客服與錯誤回報單 (私人頻道)")
    async def report(self, interaction: discord.Interaction, reason: str):
        guild = interaction.guild
        user = interaction.user

        # 設定私人頻道權限：預設全體不可見，僅回報者與機器人可見
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        # 如果有管理員身分組，允許管理員查看（可自由調整）
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel_name = f"ticket-{user.name}"
        ticket_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)

        embed = discord.Embed(
            title="🎫 錯誤回報與客服單",
            description=f"**回報者**：{user.mention}\n**回報問題**：{reason}\n\n客服人員將會盡快在此為您服務。處理完成後請輸入 `/close_ticket` 關閉頻道。",
            color=discord.Color.orange()
        )
        await ticket_channel.send(embed=embed)
        await interaction.response.send_message(f"✅ 已為您建立專屬回報頻道：{ticket_channel.mention}", ephemeral=True)

    @app_commands.command(name="close_ticket", description="關閉目前的客服頻道")
    async def close_ticket(self, interaction: discord.Interaction):
        if "ticket-" in interaction.channel.name:
            await interaction.response.send_message("🔒 本客服頻道即將於 5 秒後關閉並刪除...")
            import asyncio
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("❌ 此指令只能在客服 Ticket 頻道中使用！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))