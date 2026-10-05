import discord
from discord.ext import commands
from discord import app_commands

# CustomCheckConfirmServer
def is_guild_owner():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.guild is not None and interaction.user.id == interaction.guild.owner_id
    return app_commands.check(predicate)

class ModNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_nuke", description="頻道管理")
    @app_commands.default_permissions(administrator=True) # HiddenCommand
    @is_guild_owner() # LimitExecute
    async def mod_nuke(self, interaction: discord.Interaction):
        channel = interaction.channel
        
        await interaction.response.send_message("Channel...", ephemeral=True)
        
        try:
            new_channel = await channel.clone(reason=f" {interaction.user}  nuke Command")
            await new_channel.edit(position=channel.position)
            
            await channel.delete(reason="DeleteChannel")
            
            await new_channel.send(f" Channel {interaction.user.mention} Re-Message")
        except Exception as e:
            print(f"Nuke Failed: {e}")

    @mod_nuke.error
    async def mod_nuke_error(self, interaction: discord.Interaction, error):
        # CustomCheckError
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message("❌ PermissionCommand**Server (Owner)** ", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModNuke(bot))
