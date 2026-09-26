import os
import json
import discord
from discord import app_commands
from discord.ext import commands

# SettingsSaveChannel資料的 JSON File名稱
DATA_FILE = "farewell.json"

class Farewell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # BotStart時，AutoLoad已Save的Channel資料
        self.channels = self.load_data()

    def load_data(self):
        """Read JSON File中的ChannelSettings"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_data(self):
        """將目前的ChannelSettingsWrite JSON FileSave"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.channels, f, indent=4)

    # --------------------------------------------------
    # 1. 斜線Command：Settings道別通知Channel (僅限Manage員)
    # --------------------------------------------------
    @app_commands.command(name="set_farewell", description="Settings成員退出通知的SendChannel")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_farewell(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """
        Parameter說明：
        channel: 讓Manage員選擇要Send道別Message的目標文字Channel
        """
        guild_id = str(interaction.guild.id)
        # 將該Server的 ID 與對應的Channel ID 記錄下來
        self.channels[guild_id] = channel.id
        self.save_data()
        
        # ephemeral=True 表示這則Success提示只有Settings的Manage員自己看得到
        await interaction.response.send_message(f"[OK] 成員退出通知Channel已SuccessSettings為 {channel.mention}！", ephemeral=True)

    # --------------------------------------------------
    # 2. 斜線Command：Manual說掰掰
    # --------------------------------------------------
    @app_commands.command(name="掰掰", description="跟Server的大家或Specific成員說再見")
    async def bye(self, interaction: discord.Interaction, member: discord.Member = None):
        """
        Parameter說明：
        member: (可選) 選擇要特別說再見的Server成員
        """
        if member:
            message = f"👋 {interaction.user.mention} 依依不捨地跟 {member.mention} 說了掰掰！期待下次相見。"
        else:
            message = f"👋 {interaction.user.mention} 跟大家揮手說了掰掰！期待下次相見。"
            
        await interaction.response.send_message(message)

    # --------------------------------------------------
    # 3. Auto事件監聽：成員離開Server
    # --------------------------------------------------
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild_id = str(member.guild.id)
        
        # Check該Server是否有Settings過道別Channel
        if guild_id in self.channels:
            # 透過 ID 取得ChannelObject
            channel = self.bot.get_channel(self.channels[guild_id])
            if channel:
                # 建立一張美觀的 Embed 卡片來Display道別Message
                embed = discord.Embed(
                    title="🛫 成員離開",
                    description=f"**{member.name}** 離開了Server，祝他一切順利。",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=embed)

# 讓 main.py 能夠Load這個Module的SettingsFunction
async def setup(bot):
    await bot.add_cog(Farewell(bot))