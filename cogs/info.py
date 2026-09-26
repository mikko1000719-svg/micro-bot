import discord
from discord import app_commands
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="ServerInformation")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("CommandServer！", ephemeral=True)
            return

        #  Embed 
        embed = discord.Embed(
            title=f"🏰 {guild.name} ServerInformation",
            color=discord.Color.blue()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="", value=f"{guild.owner.mention if guild.owner else ''}", inline=True)
        embed.add_field(name="", value=f"{guild.member_count} ", inline=True)
        embed.add_field(name="Channel", value=f"{len(guild.text_channels)} ", inline=True)
        embed.add_field(name="Channel", value=f"{len(guild.voice_channels)} ", inline=True)
        embed.add_field(name="", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))