import discord
from discord.ext import commands
from discord import app_commands

class ToolAsciiText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="asciitext", description="Convert")
    @app_commands.describe(text="Convert ()")
    async def asciitext(self, interaction: discord.Interaction, text: str):
        if len(text) > 15:
            await interaction.response.send_message("[ERROR] Limit 15 ", ephemeral=True)
            return

        # 
        char_map = {
            'a': '', 'b': '', 'c': '', 'd': '', 'e': '',
            'f': '', 'g': '', 'h': '', 'i': '', 'j': '',
            'k': '', 'l': '', 'm': '', 'n': '', 'o': '',
            'p': '', 'q': '', 'r': '', 's': '', 't': '',
            'u': '', 'v': '', 'w': '', 'x': '', 'y': '', 'z': ''
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
        embed = discord.Embed(title=" Convert", description=formatted_text, color=discord.Color.purple())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ToolAsciiText(bot))