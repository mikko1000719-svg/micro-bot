# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class ModWhitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist_file = "whitelist.json"
        self._init_whitelist_file()

    def _init_whitelist_file(self):
        """初始化白名單文件"""
        if not os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def _load_whitelist(self):
        """加載白名單"""
        try:
            with open(self.whitelist_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def _save_whitelist(self, data):
        """保存白名單"""
        with open(self.whitelist_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @app_commands.command(name="whitelist_add", description="添加用戶到白名單")
    @app_commands.describe(member="要添加的成員", reason="添加原因")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def add_whitelist(self, interaction: discord.Interaction, member: discord.Member, reason: str = ""):
        whitelist = self._load_whitelist()
        guild_id_str = str(interaction.guild.id)

        if guild_id_str not in whitelist:
            whitelist[guild_id_str] = {}

        user_id_str = str(member.id)
        if user_id_str in whitelist[guild_id_str]:
            await interaction.response.send_message(f"⚠️ {member.mention} 已經在白名單中", ephemeral=True)
            return

        whitelist[guild_id_str][user_id_str] = {
            "name": member.name,
            "reason": reason,
            "added_by": str(interaction.user),
            "added_at": str(discord.utils.utcnow())
        }

        self._save_whitelist(whitelist)
        await interaction.response.send_message(f"✅ 已將 {member.mention} 添加到白名單\n原因: {reason}", ephemeral=True)

    @app_commands.command(name="whitelist_remove", description="從白名單移除用戶")
    @app_commands.describe(member="要移除的成員")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_whitelist(self, interaction: discord.Interaction, member: discord.Member):
        whitelist = self._load_whitelist()
        guild_id_str = str(interaction.guild.id)

        if guild_id_str not in whitelist:
            await interaction.response.send_message("❌ 該伺服器沒有白名單記錄", ephemeral=True)
            return

        user_id_str = str(member.id)
        if user_id_str not in whitelist[guild_id_str]:
            await interaction.response.send_message(f"⚠️ {member.mention} 不在白名單中", ephemeral=True)
            return

        del whitelist[guild_id_str][user_id_str]
        self._save_whitelist(whitelist)
        await interaction.response.send_message(f"✅ 已將 {member.mention} 從白名單移除", ephemeral=True)

    @app_commands.command(name="whitelist_list", description="查看白名單")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def list_whitelist(self, interaction: discord.Interaction):
        whitelist = self._load_whitelist()
        guild_id_str = str(interaction.guild.id)

        if guild_id_str not in whitelist or not whitelist[guild_id_str]:
            await interaction.response.send_message("📋 白名單為空", ephemeral=True)
            return

        embed = discord.Embed(
            title="📋 白名單",
            description=f"共 {len(whitelist[guild_id_str])} 位用戶",
            color=discord.Color.green()
        )

        for user_id, data in whitelist[guild_id_str].items():
            embed.add_field(
                name=f"<@{user_id}>",
                value=f"原因: {data['reason']}\n添加者: {data['added_by']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModWhitelist(bot))
