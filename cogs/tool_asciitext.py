import discord
from discord.ext import commands
from discord import app_commands

class ToolAsciiText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="asciitext", description="將英文字母Convert為醒目的粗體方塊藝術字")
    @app_commands.describe(text="要Convert的英文短句 (限英文)")
    async def asciitext(self, interaction: discord.Interaction, text: str):
        if len(text) > 15:
            await interaction.response.send_message("[ERROR] 為了版面整潔，文字長度請Limit在 15 個字元之內！", ephemeral=True)
            return

        # 簡單的英文轉方塊字對應表
        char_map = {
            'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪',
            'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯',
            'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴',
            'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹',
            'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'
        }

        result = []
        for char in text.lower():
            if char in char_map:
                result.append(char_map[char])
            elif char == ' ':
                result.append(' ')
            else:
                result.append(char)

        formatted_text = "".join(result)
        embed = discord.Embed(title="🔤 藝術字Convert結果", description=formatted_text, color=discord.Color.purple())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ToolAsciiText(bot))