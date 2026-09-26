import discord
from discord import app_commands
from discord.ext import commands
import os

class CloudCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="環境診斷", description="CheckBot目前是Run在雲端還是本地端")
    async def env_check(self, interaction: discord.Interaction):
        # 步驟 1：立即Send延遲訊號，防止 3 秒超時導致「未受回應」
        try:
            await interaction.response.defer(thinking=True)
        except discord.errors.NotFound:
            return

        # 步驟 2：偵測環境Variable
        # Render 雲端環境Default會Auto注入名為 "RENDER" 的環境Variable
        is_render = os.environ.get("RENDER") is not None
        
        if is_render:
            status_msg = "☁️ **雲端運作中**：我目前正在 Render 雲端Server上Execute，您的電腦可以放心關機！"
        else:
            status_msg = "[COMPUTER] **本地運作中**：我目前是在您的個人電腦上Execute。如果關閉電腦，我將會離線。"

        # 步驟 3：回傳診斷結果
        try:
            await interaction.followup.send(status_msg)
        except Exception as e:
            print(f"環境診斷回覆Failed: {e}")

async def setup(bot):
    await bot.add_cog(CloudCheck(bot))