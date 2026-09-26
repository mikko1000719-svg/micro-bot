import discord
from discord.ext import commands
from discord import app_commands

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_stats_channels(self, guild: discord.Guild):
        """更新或建立伺服器統計語音頻道的內部方法"""
        total_members = guild.member_count
        bot_count = sum(1 for m in guild.members if m.bot)
        human_count = total_members - bot_count

        # 定義統計頻道的名稱格式
        stats_names = {
            "total": f"[STAT] 總人數：{total_members} 人",
            "human": f"👤 真人：{human_count} 人",
            "bot": f"[BOT] 機器人：{bot_count} 個"
        }

        # 遍歷現有頻道，尋找並更新統計頻道
        for channel in guild.voice_channels:
            for key, new_name in stats_names.items():
                if key == "total" and channel.name.startswith("[STAT] 總人數"):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats 自動更新總人數")
                        return
                elif key == "human" and channel.name.startswith("👤 真人"):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats 自動更新真人數")
                        return
                elif key == "bot" and channel.name.startswith("[BOT] 機器人"):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats 自動更新機器人數")
                        return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """當新成員加入時，更新統計頻道"""
        await self.update_stats_channels(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """當成員離開時，更新統計頻道"""
        await self.update_stats_channels(member.guild)

    @app_commands.command(name="setupstats", description="[ServerStats] 自動建立伺服器即時統計語音頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def setupstats(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        # 先回覆互動避免逾時
        await interaction.response.send_message("⚙️ 正在建立 ServerStats 統計語音頻道...", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)
        }

        total_members = guild.member_count
        bot_count = sum(1 for m in guild.members if m.bot)
        human_count = total_members - bot_count

        # 建立三個數據語音頻道
        await guild.create_voice_channel(f"[STAT] 總人數：{total_members} 人", overwrites=overwrites, reason="建立總人數統計頻道")
        await guild.create_voice_channel(f"👤 真人：{human_count} 人", overwrites=overwrites, reason="建立真人統計頻道")
        await guild.create_voice_channel(f"[BOT] 機器人：{bot_count} 個", overwrites=overwrites, reason="建立機器人統計頻道")

        # 透過 followup 發送完成通知
        await interaction.followup.send("[OK] ServerStats 統計頻道建立完成！它們將會自動即時更新。", ephemeral=True)

    @setupstats.error
    async def setupstats_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 你需要「管理頻道」權限才能執行此指令！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerStats(bot))