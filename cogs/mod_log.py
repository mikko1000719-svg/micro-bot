# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

class ModLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_file = "moderation_log.json"
        self._init_log_file()

    def _init_log_file(self):
        """初始化日誌文件"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def _load_logs(self):
        """加載日誌"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def _save_logs(self, data):
        """保存日誌"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _add_log(self, guild_id, action, target, moderator, reason):
        """添加日誌"""
        logs = self._load_logs()
        guild_id_str = str(guild_id)

        if guild_id_str not in logs:
            logs[guild_id_str] = []

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "target": str(target),
            "moderator": str(moderator),
            "reason": reason
        }

        logs[guild_id_str].append(log_entry)
        self._save_logs(logs)

    @app_commands.command(name="modlog", description="查看管理日誌")
    @app_commands.describe(limit="顯示的日誌數量（預設 10）")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def view_logs(self, interaction: discord.Interaction, limit: int = 10):
        logs = self._load_logs()
        guild_id_str = str(interaction.guild.id)

        if guild_id_str not in logs or not logs[guild_id_str]:
            await interaction.response.send_message("📋 目前沒有管理日誌", ephemeral=True)
            return

        recent_logs = logs[guild_id_str][-limit:]

        embed = discord.Embed(
            title="📋 管理日誌",
            description=f"最近 {len(recent_logs)} 條記錄",
            color=discord.Color.blue()
        )

        for log in recent_logs:
            embed.add_field(
                name=f"{log['timestamp']} - {log['action']}",
                value=f"目標: {log['target']}\n管理員: {log['moderator']}\n原因: {log['reason']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModLog(bot))
