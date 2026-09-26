import discord
from discord.ext import commands
from discord import app_commands

# 1. 建立微國 5.0 專屬的分類下拉選單
class WeiGuoSettingsSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Channel廣播Settings", description="Settings微國Warning、禁言與通知的專屬Channel", emoji="📡", value="wg_channel"),
            discord.SelectOption(label="Defense靈敏度Settings", description="調整微國防洗頻閥值、連續發話上限與禁言時間", emoji="[BOLT]", value="wg_mechanism"),
            discord.SelectOption(label="成員Security白名單", description="新增或移除可略過微國Defense機制的成員", emoji="[SHIELD]", value="wg_whitelist"),
            discord.SelectOption(label="SystemRun狀態", description="查看微國 5.0 目前的各項Defense開關與狀態", emoji="[STAT]", value="wg_status")
        ]
        super().__init__(placeholder="【微國Bot 5.0】請選擇SettingsClass...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "wg_channel":
            embed = discord.Embed(title="📡 微國 5.0 - Channel廣播Settings", description="請透過Command或面板指定違規日誌與WarningMessageSend的Channel目標。", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_mechanism":
            embed = discord.Embed(title="[BOLT] 微國 5.0 - Defense靈敏度Settings", description="在此調整Auto化防洗頻的偵測敏感度與Auto禁言秒數。", color=discord.Color.orange())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_whitelist":
            embed = discord.Embed(title="[SHIELD] 微國 5.0 - 成員Security白名單", description="Manage員專屬通道：Settings不受防洗頻Limit的特權成員清單。", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_status":
            embed = discord.Embed(title="[STAT] 微國 5.0 - SystemRun狀態", description="微國核心Defense目前Run正常：[狀態: [OK] Start中]", color=discord.Color.purple())
            await interaction.response.send_message(embed=embed, ephemeral=True)

# 2. 包裝成互動Interface View
class WeiGuoShieldView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(WeiGuoSettingsSelect())

# 3. 註冊斜線Command
class WeiGuoShield(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="weiguosetup", description="[微國Bot 5.0] 開啟智慧Defense與ServerSecurityManage面板")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def weiguosetup(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="[SHIELD] 微國Bot 5.0 | 智慧SecurityDefense中樞",
            description=(
                "**【微國 5.0 設置重點說明】**\n"
                "1. 本Defense核心Default為 **OFF** 狀態，需點擊下方選單開啟。\n"
                "2. 請先Settings違規通知Receive的日誌Channel。\n"
                "3. 白名單成員將Auto略過Bot的Auto防洗頻機制。\n"
                "4. 請確保微國 5.0 的身份組層級高於一般成員，以確保順利ExecuteDefense。\n\n"
                "👉 **請從下方選單選擇您要進行的微國 5.0 Settings項目：**"
            ),
            color=discord.Color.from_rgb(47, 49, 54)
        )
        embed.set_footer(text=f"微國Bot 5.0 System • 調用者：{interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        
        view = WeiGuoShieldView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @weiguosetup.error
    async def weiguosetup_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("[ERROR] Permission不足！你需要「ManageServer」Permission才能開啟微國 5.0 Defense面板。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(WeiGuoShield(bot))