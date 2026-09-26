import discord
from discord.ext import commands
from datetime import timedelta
from collections import defaultdict

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Format: {user_id: {"content": , "count": , "burst": Message}}
        self.user_data = defaultdict(lambda: {"content": "", "count": 0, "burst": 0})

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild or message.author.guild_permissions.administrator:
            return

        user_id = message.author.id
        content = message.content.strip()
        data = self.user_data[user_id]

        # 1.  ()
        if data["content"] == content:
            data["count"] += 1
        else:
            data["content"] = content
            data["count"] = 1

        if data["count"] >= 3:
            try:
                await message.author.timeout(timedelta(hours=24), reason=" 5.0： 3 ")
                await message.channel.send(f"🚨 {message.author.mention} Auto 24 。")
                data["count"] = 0 # 
            except Exception as e:
                print(f"Failed: {e}")
                
        # 2.  (SendMessage)
        # Requirement， 5  10 
        data["burst"] += 1
        # Defense...

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))