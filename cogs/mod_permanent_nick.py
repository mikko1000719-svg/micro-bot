import os
import json
import discord
from discord.ext import commands
from discord import app_commands

DATA_FILE = "jose_nicks.json"

# CustomCheckConfirmServer
def is_guild_owner():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.guild is not None and interaction.user.id == interaction.guild.owner_id
    return app_commands.check(predicate)

class PermanentNick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.locked_nicks = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    data = {}
                    for g_id, users in raw_data.items():
                        data[int(g_id)] = {int(u_id): nick for u_id, nick in users.items()}
                    return data
            except Exception as e:
                print(f"[jOSeSystem] ReadFailed: {e}")
        return {}

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.locked_nicks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[jOSeSystem] SaveFailed: {e}")

    @app_commands.command(name="setpermanentnick", description="[jOSeSystem] SettingsPermanent")
    @app_commands.describe(member="Parameter description", nickname="Permanent")
    @app_commands.default_permissions(administrator=True) # HiddenCommand
    @is_guild_owner() # LimitExecute
    async def setpermanentnick(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        guild_id = interaction.guild.id
        
        if guild_id not in self.locked_nicks:
            self.locked_nicks[guild_id] = {}
            
        self.locked_nicks[guild_id][member.id] = nickname
        self.save_data() 
        
        try:
            await member.edit(nick=nickname, reason=f"Server {interaction.user}  jOSe PermanentSystem")
            
            embed = discord.Embed(
                title="🔒 jOSe System - Permanent",
                description=f"Success **{member.mention}** \n`{nickname}`\n\n*✅ Write jOSe PermanentDatabaseBot*",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ PermissionManagePermission", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error{e}", ephemeral=True)

    @setpermanentnick.error
    async def setpermanentnick_error(self, interaction: discord.Interaction, error):
        # CustomCheckError
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message("❌ PermissionCommand**Server (Owner)** ", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        guild_id = after.guild.id
        
        if guild_id not in self.locked_nicks:
            return
            
        if after.id not in self.locked_nicks[guild_id]:
            return
            
        target_nick = self.locked_nicks[guild_id][after.id]
        
        if after.display_name != target_nick:
            try:
                await after.edit(nick=target_nick, reason="[jOSeSystem] PermanentSystemAuto")
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(PermanentNick(bot))
