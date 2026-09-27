import discord
from discord.ext import commands
from discord import app_commands

# CustomCheckConfirmServer
def is_guild_owner():
    def predicate(interaction: discord.Interaction) -> bool:
        # ServerExecute ID Server ID
        return interaction.guild is not None and interaction.user.id == interaction.guild.owner_id
    return app_commands.check(predicate)

class ModAntiBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.antibot_enabled = {}

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot and self.antibot_enabled.get(member.guild.id, False):
            try:
                await member.kick(reason="Anti-Bot SystemAutoBot")
            except Exception as e:
                print(f" BOT Failed: {e}")

    @app_commands.command(name="mod_antibot", description="BotAuto BOT")
    @app_commands.describe(enable="True Protection / False Protection")
    @app_commands.default_permissions(administrator=True) # HiddenCommand
    @is_guild_owner() # LimitExecute
    async def mod_antibot(self, interaction: discord.Interaction, enable: bool):
        self.antibot_enabled[interaction.guild.id] = enable
        status = "✅ " if enable else "🛑 "
        msg = f"🛡️ **Bot (Anti-Bot)  {status}**\n"
        if enable:
            msg += "SystemAutoServerBot"
        
        await interaction.response.send_message(msg, ephemeral=True)

    @mod_antibot.error
    async def mod_antibot_error(self, interaction: discord.Interaction, error):
        # CustomCheckError
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message("❌ PermissionCommand**Server (Owner)** ", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModAntiBot(bot))
