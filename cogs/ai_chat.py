# -*- coding: utf-8 -*-
import discord
from discord import app_commands
from discord.ext import commands
from google import genai
import os
import traceback
import asyncio  # 引入非同步控制模組

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = None
        
        # 1. 讀取並確認 API Key
        api_key = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")
        
        if api_key:
            masked_key = api_key[:5] + "..." if len(api_key) > 5 else "***"
            print(f"[AI System] Successfully loaded environment variable! Key prefix: {masked_key} (length: {len(api_key)})", flush=True)
        else:
            print("[ERROR] [AI System] Warning: GEMINI_API_KEY not found in Render!", flush=True)
            return
            
        try:
            # 2. 初始化 Gemini Client
            self.client = genai.Client(api_key=api_key)
            print("[OK] [AI System] Successfully initialized Gemini Client!", flush=True)

        except Exception as e:
            print(f"[ERROR] [AI System] Initialization failed: {e}", flush=True)
            traceback.print_exc()

    @app_commands.command(name="ai", description="與 AI 進行對話")
    @app_commands.describe(prompt="你想對 AI 說的話")
    async def ai_chat(self, interaction: discord.Interaction, prompt: str):
        # 立即延遲回覆，避免 Discord 發生逾時錯誤
        await interaction.response.defer(thinking=True)

        if not self.client:
            await interaction.followup.send("[ERROR] AI client not initialized: Please check API Key settings in Render!")
            return

        try:
            # 【關鍵修復】使用 asyncio.to_thread 把同步的網路請求丟到背景執行緒
            # 這樣才不會卡死 Discord 的事件迴圈，避免發生 heartbeat blocked 斷線錯誤
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            if response and response.text:
                reply_text = response.text
                
                # 防護機制：避免超過 Discord 2000 字元限制
                if len(reply_text) > 1900:
                    reply_text = reply_text[:1900] + "\n\n...(字數過長，已自動截斷)"
                    
                await interaction.followup.send(f"**問：** {prompt}\n\n**答：**\n{reply_text}")
            else:
                await interaction.followup.send("[ERROR] AI currently has no response, please try again later.")

        except Exception as e:
            print("[ERROR] [AI System] Error generating response:", flush=True)
            traceback.print_exc()
            await interaction.followup.send(f"[ERROR] Error calling AI: `{e}`")

async def setup(bot):
    await bot.add_cog(AIChat(bot))
