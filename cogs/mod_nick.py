import discord
from discord.ext import commands
from discord import app_commands

class ModNick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mod_nick", description="ServerDisplay")
    @app_commands.describe(member="Parameter description", nickname=" (Custom)")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def mod_nick(self, interaction: discord.Interaction, member: discord.Member, nickname: str = None):
        try:
            await member.edit(nick=nickname, reason=f" {interaction.user} Command")
            if nickname:
                await interaction.response.send_message(f" Success {member.mention}  **{nickname}**")
            else:
                await interaction.response.send_message(f"[SWITCH] Success {member.mention} ")
        except Exception as e:
            await interaction.response.send_message(f"❌ FailedBot{e}", ephemeral=True)

    @mod_nick.error
    async def mod_nick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ ManagePermissionCommand", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModNick(bot))
