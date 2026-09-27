import os
import json
import discord
from discord import app_commands
from discord.ext import commands

# SettingsSaveChannel JSON File
DATA_FILE = "farewell.json"

class Farewell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # BotStartAutoLoadSaveChannel
        self.channels = self.load_data()

    def load_data(self):
        """Read JSON FileChannelSettings"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_data(self):
        """ChannelSettingsWrite JSON FileSave"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.channels, f, indent=4)

    # --------------------------------------------------
    # 1. CommandSettingsChannel (Manage)
    # --------------------------------------------------
    @app_commands.command(name="set_farewell", description="SettingsSendChannel")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_farewell(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """
        Parameter
        channel: ManageSendMessageChannel
        """
        guild_id = str(interaction.guild.id)
        # Server ID Channel ID 
        self.channels[guild_id] = channel.id
        self.save_data()
        
        # ephemeral=True SuccessSettingsManage
        await interaction.response.send_message(f"[OK] ChannelSuccessSettings {channel.mention}", ephemeral=True)

    # --------------------------------------------------
    # 2. CommandManual
    # --------------------------------------------------
    @app_commands.command(name="Parameter description", description="ServerSpecific")
    async def bye(self, interaction: discord.Interaction, member: discord.Member = None):
        """
        Parameter
        member: () Server
        """
        if member:
            message = f" {interaction.user.mention}  {member.mention} "
        else:
            message = f" {interaction.user.mention} "
            
        await interaction.response.send_message(message)

    # --------------------------------------------------
    # 3. AutoServer
    # --------------------------------------------------
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild_id = str(member.guild.id)
        
        # CheckServerSettingsChannel
        if guild_id in self.channels:
            #  ID ChannelObject
            channel = self.bot.get_channel(self.channels[guild_id])
            if channel:
                #  Embed DisplayMessage
                embed = discord.Embed(
                    title=" ",
                    description=f"**{member.name}** Server",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=embed)

#  main.py LoadModuleSettingsFunction
async def setup(bot):
    await bot.add_cog(Farewell(bot))