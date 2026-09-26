import discord
from discord.ext import commands
from discord import app_commands

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_stats_channels(self, guild: discord.Guild):
        """Update或建立Server統計語音Channel的內部Method"""
        total_members = guild.member_count
        bot_count = sum(1 for m in guild.members if m.bot)
        human_count = total_members - bot_count

        # 定義統計Channel的名稱Format
        stats_names = {
            "total": f"[STAT] 總人數：{total_members} 人",
            "human": f"👤 真人：{human_count} 人",
            "bot": f"[BOT] Bot：{bot_count} 個"
        }

        # 遍歷現有Channel，尋找並Update統計Channel
        for channel in guild.voice_channels:
            for key, new_name in stats_names.items():
                if key == "total" and channel.name.startswith("[STAT] 總人數"):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats AutoUpdate總人數")
                        return
                elif key == "human" and channel.name.startswith("👤 真人"):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats AutoUpdate真人數")
                        return
                elif key == "bot" and channel.name.startswith("[BOT] Bot"):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats AutoUpdateBot數")
                        return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """當新成員加入時，Update統計Channel"""
        await self.update_stats_channels(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """當成員離開時，Update統計Channel"""
        await self.update_stats_channels(member.guild)

    @app_commands.command(name="setupstats", description="[ServerStats] Auto建立ServerReal-time統計語音Channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def setupstats(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        # 先回覆互動避免逾時
        await interaction.response.send_message("⚙️ 正在建立 ServerStats 統計語音Channel...", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)
        }

        total_members = guild.member_count
        bot_count = sum(1 for m in guild.members if m.bot)
        human_count = total_members - bot_count

        # 建立三個數據語音Channel
        await guild.create_voice_channel(f"[STAT] 總人數：{total_members} 人", overwrites=overwrites, reason="建立總人數統計Channel")
        await guild.create_voice_channel(f"👤 真人：{human_count} 人", overwrites=overwrites, reason="建立真人統計Channel")
        await guild.create_voice_channel(f"[BOT] Bot：{bot_count} 個", overwrites=overwrites, reason="建立Bot統計Channel")

        # 透過 followup SendComplete通知
        await interaction.followup.send("[OK] ServerStats 統計Channel建立Complete！它們將會AutoReal-timeUpdate。", ephemeral=True)

    @setupstats.error
    async def setupstats_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「ManageChannel」Permission才能Execute此Command！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerStats(bot))