import os
import json
import discord
from discord import app_commands
from discord.ext import commands

DATA_FILE = "levels.json"

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_data = self.load_data()

    def load_data(self):
        """ JSON FileLoad"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"SystemRead levels.json FailedInitialize: {e}")
                return {}
        return {}

    def save_data(self):
        """Save JSON File"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.xp_data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # BotMessage
        if message.author.bot:
            return

        user_id = str(message.author.id)
        #  +1
        self.xp_data[user_id] = self.xp_data.get(user_id, 0) + 1
        self.save_data()

        xp = self.xp_data[user_id]
        level = int(xp**0.5) // 5

        #  25 
        if xp % 25 == 0:
            await message.channel.send(f"🎉  {message.author.mention} {level} (: {xp})")

    @app_commands.command(name="rank", description="指令說明")
    async def rank(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        xp = self.xp_data.get(user_id, 0)
        level = int(xp**0.5) // 5
        await interaction.response.send_message(f"📊 {interaction.user.name} {level} {xp}", ephemeral=True)

async def setup(bot):
    """ Cog Load"""
    await bot.add_cog(Leveling(bot))