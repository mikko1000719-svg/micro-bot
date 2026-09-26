import discord
from discord.ext import commands
from discord import app_commands

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_stats_channels(self, guild: discord.Guild):
        """UpdateServerChannelMethod"""
        total_members = guild.member_count
        bot_count = sum(1 for m in guild.members if m.bot)
        human_count = total_members - bot_count

        # ChannelFormat
        stats_names = {
            "total": f"[STAT] ：{total_members} ",
            "human": f"👤 ：{human_count} ",
            "bot": f"[BOT] Bot：{bot_count} "
        }

        # Channel，UpdateChannel
        for channel in guild.voice_channels:
            for key, new_name in stats_names.items():
                if key == "total" and channel.name.startswith("[STAT] "):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats AutoUpdate")
                        return
                elif key == "human" and channel.name.startswith("👤 "):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats AutoUpdate")
                        return
                elif key == "bot" and channel.name.startswith("[BOT] Bot"):
                    if channel.name != new_name:
                        await channel.edit(name=new_name, reason="ServerStats AutoUpdateBot")
                        return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """，UpdateChannel"""
        await self.update_stats_channels(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """，UpdateChannel"""
        await self.update_stats_channels(member.guild)

    @app_commands.command(name="setupstats", description="[ServerStats] AutoServerReal-timeChannel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def setupstats(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        # 
        await interaction.response.send_message("⚙️  ServerStats Channel...", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)
        }

        total_members = guild.member_count
        bot_count = sum(1 for m in guild.members if m.bot)
        human_count = total_members - bot_count

        # Channel
        await guild.create_voice_channel(f"[STAT] ：{total_members} ", overwrites=overwrites, reason="Channel")
        await guild.create_voice_channel(f"👤 ：{human_count} ", overwrites=overwrites, reason="Channel")
        await guild.create_voice_channel(f"[BOT] Bot：{bot_count} ", overwrites=overwrites, reason="BotChannel")

        #  followup SendComplete
        await interaction.followup.send("[OK] ServerStats ChannelComplete！AutoReal-timeUpdate。", ephemeral=True)

    @setupstats.error
    async def setupstats_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] 「ManageChannel」PermissionExecuteCommand！", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerStats(bot))