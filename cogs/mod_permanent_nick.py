import os
import json
import discord
from discord.ext import commands
from discord import app_commands

DATA_FILE = "jose_nicks.json"

# 建立CustomCheck器：Confirm使用者是否為Server擁有者
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
                print(f"[jOSeSystem] Read資料Failed: {e}")
        return {}

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.locked_nicks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[jOSeSystem] Save資料Failed: {e}")

    @app_commands.command(name="setpermanentnick", description="[jOSeSystem] Settings某成員的Permanent暱稱（支援重啟持久化保存）")
    @app_commands.describe(member="要鎖定暱稱的成員", nickname="要強制套用的Permanent暱稱")
    @app_commands.default_permissions(administrator=True) # 對一般成員HiddenCommand
    @is_guild_owner() # 核心：Limit只有擁有者可以Execute
    async def setpermanentnick(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        guild_id = interaction.guild.id
        
        if guild_id not in self.locked_nicks:
            self.locked_nicks[guild_id] = {}
            
        self.locked_nicks[guild_id][member.id] = nickname
        self.save_data() 
        
        try:
            await member.edit(nick=nickname, reason=f"由Server擁有者 {interaction.user} 套用 jOSe Permanent暱稱System")
            
            embed = discord.Embed(
                title="[LOCK] jOSe System - Permanent暱稱已鎖定",
                description=f"Success將 **{member.mention}** 的暱稱鎖定為：\n`{nickname}`\n\n*[OK] 此資料已Write jOSe PermanentDatabase，Bot重啟後依然有效。*",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("[ERROR] Permission不足！我的身份組必須高於該成員，且擁有「Manage暱稱」Permission。", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"[ERROR] 發生Error：{e}", ephemeral=True)

    @setpermanentnick.error
    async def setpermanentnick_error(self, interaction: discord.Interaction, error):
        # 攔截我們的CustomCheckError
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message("[ERROR] Permission不足！此Command**僅限Server擁有者 (Owner)** 使用！", ephemeral=True)

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
                await after.edit(nick=target_nick, reason="[jOSeSystem] 偵測到違規更改Permanent暱稱，SystemAuto還原")
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(PermanentNick(bot))
