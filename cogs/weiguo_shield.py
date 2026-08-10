import discord
from discord.ext import commands
from discord import app_commands

# 1. 建立微國 5.0 專屬的分類下拉選單
class WeiGuoSettingsSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="頻道廣播設定", description="設定微國警告、禁言與通知的專屬頻道", emoji="📡", value="wg_channel"),
            discord.SelectOption(label="防護靈敏度設定", description="調整微國防洗頻閥值、連續發話上限與禁言時間", emoji="⚡", value="wg_mechanism"),
            discord.SelectOption(label="成員安全白名單", description="新增或移除可略過微國防護機制的成員", emoji="🛡️", value="wg_whitelist"),
            discord.SelectOption(label="系統運行狀態", description="查看微國 5.0 目前的各項防護開關與狀態", emoji="📊", value="wg_status")
        ]
        super().__init__(placeholder="【微國機器人 5.0】請選擇設定類別...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "wg_channel":
            embed = discord.Embed(title="📡 微國 5.0 - 頻道廣播設定", description="請透過指令或面板指定違規日誌與警告訊息發送的頻道目標。", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_mechanism":
            embed = discord.Embed(title="⚡ 微國 5.0 - 防護靈敏度設定", description="在此調整自動化防洗頻的偵測敏感度與自動禁言秒數。", color=discord.Color.orange())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_whitelist":
            embed = discord.Embed(title="🛡️ 微國 5.0 - 成員安全白名單", description="管理員專屬通道：設定不受防洗頻限制的特權成員清單。", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected == "wg_status":
            embed = discord.Embed(title="📊 微國 5.0 - 系統運行狀態", description="微國核心防護目前運行正常：[狀態: 🟢 啟動中]", color=discord.Color.purple())
            await interaction.response.send_message(embed=embed, ephemeral=True)

# 2. 包裝成互動介面 View
class WeiGuoShieldView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(WeiGuoSettingsSelect())

# 3. 註冊斜線指令
class WeiGuoShield(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="weiguosetup", description="[微國機器人 5.0] 開啟智慧防護與伺服器安全管理面板")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def weiguosetup(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛡️ 微國機器人 5.0 | 智慧安全防護中樞",
            description=(
                "**【微國 5.0 設置重點說明】**\n"
                "1. 本防護核心預設為 **OFF** 狀態，需點擊下方選單開啟。\n"
                "2. 請先設定違規通知接收的日誌頻道。\n"
                "3. 白名單成員將自動略過機器人的自動防洗頻機制。\n"
                "4. 請確保微國 5.0 的身份組層級高於一般成員，以確保順利執行防護。\n\n"
                "👉 **請從下方選單選擇您要進行的微國 5.0 設定項目：**"
            ),
            color=discord.Color.from_rgb(47, 49, 54)
        )
        embed.set_footer(text=f"微國機器人 5.0 系統 • 調用者：{interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        
        view = WeiGuoShieldView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @weiguosetup.error
    async def weiguosetup_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ 權限不足！你需要「管理伺服器」權限才能開啟微國 5.0 防護面板。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(WeiGuoShield(bot))