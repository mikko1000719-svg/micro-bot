import os
import json
import discord
from discord import app_commands
from discord.ext import commands

DATA_FILE = "welcome.json"

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.channels, f, indent=4)

    @app_commands.command(name="set_welcome", description="SettingsAuto歡迎Message的SendChannel")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        self.channels[guild_id] = channel.id
        self.save_data()
        await interaction.response.send_message(f"[OK] Auto歡迎Channel已SuccessSettings為 {channel.mention}！", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_id = str(member.guild.id)
        if guild_id in self.channels:
            channel = self.bot.get_channel(self.channels[guild_id])
            if channel:
                embed = discord.Embed(
                    title="[PARTY] 歡迎加入！",
                    description=f"歡迎 {member.mention} 來到 **{member.guild.name}**！希望能在這裡玩得開心。",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))