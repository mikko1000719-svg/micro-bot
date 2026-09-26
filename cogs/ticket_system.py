import asyncio
import discord
from discord import app_commands
from discord.ext import commands

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def notify_owner(self, guild: discord.Guild, user: discord.User, reason: str, channel: discord.TextChannel):
        """輔助函式：當有新 Ticket 建立時，私訊通知唯一擁有者"""
        owner_cog = self.bot.get_cog("OwnerDM")
        if owner_cog and owner_cog.owner_id:
            try:
                owner = await self.bot.fetch_user(owner_cog.owner_id)
                if owner:
                    embed = discord.Embed(
                        title="🎫 收到新的客服與Error回報單",
                        description=f"**來源Server**：{guild.name}\n**回報成員**：{user.mention} (`{user.id}`)\n**回報內容**：{reason}\n**Channel位置**：{channel.mention}",
                        color=discord.Color.gold()
                    )
                    await owner.send(embed=embed)
            except Exception as e:
                print(f"[TicketSystem] 通知 Owner Failed: {e}")

    @app_commands.command(name="report", description="建立客服與Error回報單 (私人Channel)")
    async def report(self, interaction: discord.Interaction, reason: str):
        guild = interaction.guild
        user = interaction.user

        # Settings私人ChannelPermission：Default全體不可見，僅回報者與Bot可見
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        # 如果有Manage員身分組，允許Manage員查看
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel_name = f"ticket-{user.name}"
        ticket_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)

        embed = discord.Embed(
            title="🎫 Error回報與客服單",
            description=f"**回報者**：{user.mention}\n**回報問題**：{reason}\n\n客服人員將會盡快在此為您服務。ProcessComplete後請輸入 `/close_ticket` 關閉Channel。",
            color=discord.Color.orange()
        )
        await ticket_channel.send(embed=embed)
        await interaction.response.send_message(f"[OK] 已為您建立專屬回報Channel：{ticket_channel.mention}", ephemeral=True)

        # 觸發通知唯一擁有者
        await self.notify_owner(guild, user, reason, ticket_channel)

    @app_commands.command(name="close_ticket", description="關閉目前的客服Channel")
    async def close_ticket(self, interaction: discord.Interaction):
        if "ticket-" in interaction.channel.name:
            await interaction.response.send_message("[LOCK] 本客服Channel即將於 5 秒後關閉並Delete...")
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("[ERROR] 此Command只能在客服 Ticket Channel中使用！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
