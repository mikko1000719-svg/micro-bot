import os
import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai

class AIChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.model = None
        self.init_error = None

        # 讀取並淨化 GEMINI_API_KEY
        raw_key = os.getenv("GEMINI_API_KEY", "")
        self.api_key = raw_key.strip().strip('"').strip("'")

        if not self.api_key:
            self.init_error = "伺服器未設定有效的 GEMINI_API_KEY，請檢查環境變數。"
            print(f"❌ {self.init_error}")
            return

        try:
            genai.configure(api_key=self.api_key)
            # 使用正確的標準模型名稱，解決 404 問題
            self.model = genai.GenerativeModel("models/gemini-1.5-flash")
            print("✅ [AI 模組] Gemini 模型初始化成功！")
        except Exception as e:
            self.init_error = f"Gemini SDK 設定失敗: {e}"
            print(f"❌ [AI 模組] {self.init_error}")

    @app_commands.command(name="ai", description="與 AI 進行對話")
    @app_commands.describe(prompt="請輸入您想對 AI 說的話")
    async def ai(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer(thinking=True)

        if not self.model or self.init_error:
            await interaction.followup.send(f"❌ **AI 啟動失敗**\n原因：`{self.init_error}`")
            return

        try:
            response = self.model.generate_content(prompt)
            reply_text = response.text if response.text else "⚠️ AI 未回傳內容。"
            if len(reply_text) > 1900:
                reply_text = reply_text[:1900] + "\n...(已截斷)"
            await interaction.followup.send(f"🤖 **AI 回應**：\n{reply_text}")
        except Exception as e:
            await interaction.followup.send(f"❌ 呼叫 AI 發生例外：{e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(AIChat(bot))