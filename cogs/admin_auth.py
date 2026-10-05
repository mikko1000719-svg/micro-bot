# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import json
import os
import time
import random
import string

class AdminAuth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auth_file = "admin_auth.json"
        self._init_auth_file()

    def _init_auth_file(self):
        """初始化驗證碼存儲文件"""
        if not os.path.exists(self.auth_file):
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def _load_auth_data(self):
        """加載驗證碼數據"""
        try:
            with open(self.auth_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def _save_auth_data(self, data):
        """保存驗證碼數據"""
        with open(self.auth_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _generate_code(self, length=8):
        """生成隨機驗證碼"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def _cleanup_expired_codes(self, data):
        """清理過期的驗證碼"""
        current_time = time.time()
        expiry_time = 300  # 5分鐘 = 300秒

        cleaned_data = {}
        for guild_id, code_data in data.items():
            if current_time - code_data['timestamp'] < expiry_time:
                cleaned_data[guild_id] = code_data

        return cleaned_data

    @commands.Cog.listener()
    async def on_ready(self):
        print("[OK] Admin Auth module loaded")

    @commands.command(name='generate_admin_code')
    @commands.has_permissions(administrator=True)
    async def generate_admin_code(self, ctx):
        """生成管理面板登入驗證碼"""
        # 清理過期驗證碼
        data = self._load_auth_data()
        data = self._cleanup_expired_codes(data)

        # 生成新驗證碼
        guild_id = str(ctx.guild.id)
        code = self._generate_code()

        data[guild_id] = {
            'code': code,
            'timestamp': time.time(),
            'user_id': str(ctx.author.id)
        }

        self._save_auth_data(data)

        # 發送驗證碼給管理員
        embed = discord.Embed(
            title="🔐 管理面板驗證碼",
            description=f"你的驗證碼是：**{code}**\n\n此驗證碼將在 5 分鐘後過期。\n請在管理面板中輸入此驗證碼。",
            color=discord.Color.blue()
        )
        embed.add_field(name="伺服器 ID", value=guild_id, inline=False)
        embed.add_field(name="有效時間", value="5 分鐘", inline=False)
        embed.set_footer(text="請勿將此驗證碼分享給他人")

        await ctx.author.send(embed=embed)
        await ctx.send("✅ 驗證碼已發送到你的私訊中！")

    @generate_admin_code.error
    async def generate_admin_code_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ 只有管理員才能使用此指令！")
        else:
            await ctx.send(f"❌ 發生錯誤：{error}")

async def setup(bot):
    await bot.add_cog(AdminAuth(bot))
