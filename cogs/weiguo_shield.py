import discord
from discord.ext import commands
from discord import app_commands

# 1.  5.0 
class WeiGuoSettingsSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="ChannelSettings", description="SettingsWarning、Channel", emoji="📡", value="wg_channel"),
            discord.SelectOption(label="DefenseSettings", description="、", emoji="[BOLT]", value="wg_mechanism"),
            discord.SelectOption(label="Security", description="Defense", emoji="[SHIELD]", value="wg_whitelist"),
            discord.SelectOption(label="SystemRun", description=" 5.0 Defense", emoji="[STAT]", value="wg_status")
        ]
        super().__init__(placeholder="【Bot 5.0】SettingsClass...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "wg_channel":
            embed = discord.Embed(title="📡  5.0 - ChannelSettings", description="CommandWarningMessageSendChannel。", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_mechanism":
            embed = discord.Embed(title="[BOLT]  5.0 - DefenseSettings", description="AutoAuto。", color=discord.Color.orange())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_whitelist":
            embed = discord.Embed(title="[SHIELD]  5.0 - Security", description="Manage：SettingsLimit。", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_status":
            embed = discord.Embed(title="[STAT]  5.0 - SystemRun", description="DefenseRun：[: [OK] Start]", color=discord.Color.purple())
            await interaction.response.send_message(embed=embed, ephemeral=True)

# 2. Interface View
class WeiGuoShieldView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(WeiGuoSettingsSelect())

# 3. Command
class WeiGuoShield(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="weiguosetup", description="[Bot 5.0] DefenseServerSecurityManage")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def weiguosetup(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="[SHIELD] Bot 5.0 | SecurityDefense",
            description=(
                "**【 5.0 】**\n"
                "1. DefenseDefault **OFF** ，。\n"
                "2. SettingsReceiveChannel。\n"
                "3. AutoBotAuto。\n"
                "4.  5.0 ，ExecuteDefense。\n\n"
                "👉 ** 5.0 Settings：**"
            ),
            color=discord.Color.from_rgb(47, 49, 54)
        )
        embed.set_footer(text=f"Bot 5.0 System • ：{interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        
        view = WeiGuoShieldView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @weiguosetup.error
    async def weiguosetup_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] Permission！「ManageServer」Permission 5.0 Defense。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(WeiGuoShield(bot))