import discord
from discord.ext import commands
from discord import app_commands

class CmdEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="embed", description=" Embed ")
    @app_commands.describe(title="", description="", color=" (: red, blue, green)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def custom_embed(self, interaction: discord.Interaction, title: str, description: str, color: str = "blue"):
        # Convert
        color_map = {
            "red": discord.Color.red(),
            "blue": discord.Color.blue(),
            "green": discord.Color.green(),
            "gold": discord.Color.gold(),
            "purple": discord.Color.purple(),
            "orange": discord.Color.orange()
        }
        embed_color = color_map.get(color.lower(), discord.Color.blue())
        
        embed = discord.Embed(title=title, description=description.replace("\\n", "\n"), color=embed_color)
        embed.set_footer(text=f"{interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("[OK] SuccessSend", ephemeral=True)

    @custom_embed.error
    async def embed_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] ManageMessagePermission Embed ", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdEmbed(bot))