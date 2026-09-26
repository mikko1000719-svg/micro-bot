# -*- coding: utf-8 -*-
import discord
from discord import app_commands
from discord.ext import commands
from google import genai
import os
import traceback
import asyncio  # Import async control module

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = None

        # 1. Read and confirm API Key
        api_key = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")

        if api_key:
            masked_key = api_key[:5] + "..." if len(api_key) > 5 else "***"
            print(f"[AI System] Successfully loaded environment variable! Key prefix: {masked_key} (length: {len(api_key)})", flush=True)
        else:
            print("[ERROR] [AI System] Warning: GEMINI_API_KEY not found in Render!", flush=True)
            return

        try:
            # 2. Initialize Gemini Client
            self.client = genai.Client(api_key=api_key)
            print("[OK] [AI System] Successfully initialized Gemini Client!", flush=True)

        except Exception as e:
            print(f"[ERROR] [AI System] Initialization failed: {e}", flush=True)
            traceback.print_exc()

    @app_commands.command(name="ai", description="Chat with AI")
    @app_commands.describe(prompt="What you want to say to AI")
    async def ai_chat(self, interaction: discord.Interaction, prompt: str):
        # Immediately defer response to avoid Discord timeout error
        await interaction.response.defer(thinking=True)

        if not self.client:
            await interaction.followup.send("[ERROR] AI client not initialized: Please check API Key settings in Render!")
            return

        try:
            # [Key Fix] Use asyncio.to_thread to put synchronous network requests to background thread
            # This won't block Discord's event loop, avoiding heartbeat blocked disconnection error
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model='gemini-2.5-flash',
                contents=prompt
            )

            if response and response.text:
                reply_text = response.text

                # Defense mechanism: avoid exceeding Discord 2000 character limit
                if len(reply_text) > 1900:
                    reply_text = reply_text[:1900] + "\n\n...(text too long, automatically truncated)"

                await interaction.followup.send(f"**Question:** {prompt}\n\n**Answer:**\n{reply_text}")
            else:
                await interaction.followup.send("[ERROR] AI currently has no response, please try again later.")

        except Exception as e:
            print("[ERROR] [AI System] Error generating response:", flush=True)
            traceback.print_exc()
            await interaction.followup.send(f"[ERROR] Error calling AI: `{e}`")

async def setup(bot):
    await bot.add_cog(AIChat(bot))
