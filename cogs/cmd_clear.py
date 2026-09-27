import discord
from discord.ext import commands
from discord import app_commands

class CmdClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="ChannelMessage")
    @app_commands.describe(amount="Message (1  100 )")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("❌  1  100 Message", ephemeral=True)
            return
            
        #  interaction
        await interaction.response.defer(ephemeral=True)
        
        # ExecuteDelete
        deleted = await interaction.channel.purge(limit=amount)
        
        await interaction.followup.send(f"🧹 Success **{len(deleted)}** Message", ephemeral=True)

    @clear.error
    async def clear_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManageMessagePermissionMessage", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdClear(bot))