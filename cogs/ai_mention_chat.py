# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError
import os
import traceback
import asyncio
import time
import sqlite3

# Default persona (used if database hasn't been populated with persona via chat)
DEFAULT_PERSONA = "You are a polite and helpful Discord chat assistant, please answer user's questions seriously."

class AIMentionChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clients = []
        self.current_index = 0

        # 🤖 Bot anti-infinite conversation counter {channel_id: {"count": int, "last_time": float}}
        self.bot_interaction_tracker = {}

        # 💾 Initialize SQLite permanent memory and settings database
        self.db_path = "chat_memory.db"
        self._init_db()

        # Read GEMINI_API_KEY2 to GEMINI_API_KEY11 in sequence (10 groups)
        key_env_names = [f"GEMINI_API_KEY{i}" for i in range(2, 12)]

        for name in key_env_names:
            api_key = os.getenv(name, "").strip().strip('"').strip("'")
            if api_key:
                try:
                    client = genai.Client(api_key=api_key)
                    self.clients.append((name, client))
                    print(f"[OK] [Multi-Key System] Successfully loaded {name}", flush=True)
                except Exception as e:
                    print(f"[ERROR] [Multi-Key System] {name} initialization failed: {e}", flush=True)
            else:
                print(f"[WARNING] [Multi-Key System] Environment variable {name} not found", flush=True)

        if not self.clients:
            print("[ERROR] [Multi-Key System] Warning: No API Keys successfully loaded!", flush=True)

        print("[OK] [Multi-Key System] Initialization complete", flush=True)

    def _init_db(self):
        """Create SQLite database (conversation history + bot persona settings)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Conversation history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER,
                    speaker TEXT,
                    content TEXT,
                    timestamp REAL
                )
            """)
            # Settings table (used to store dynamic persona)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bot_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.commit()
        print("[DB] [Permanent Memory and Settings System] SQLite database initialized successfully!", flush=True)

    def get_persona(self) -> str:
        """Read current AI persona settings from SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM bot_settings WHERE key = 'persona'")
            row = cursor.fetchone()
            if row and row[0]:
                return row[0]
        return DEFAULT_PERSONA

    def set_persona(self, new_persona: str):
        """Write new AI persona settings to SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bot_settings (key, value)
                VALUES ('persona', ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """, (new_persona,))
            conn.commit()

    def save_chat_memory(self, channel_id: int, speaker: str, content: str):
        """Save conversation to SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (channel_id, speaker, content, timestamp) VALUES (?, ?, ?, ?)",
                (channel_id, speaker, content, time.time())
            )
            conn.commit()

    def load_chat_memory(self, channel_id: int, limit: int = 8) -> str:
        """Read recent N conversation history from SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT speaker, content FROM chat_history WHERE channel_id = ? ORDER BY id DESC LIMIT ?",
                (channel_id, limit)
            )
            rows = cursor.fetchall()

        if not rows:
            return ""

        rows.reverse()
        history_lines = [f"{speaker}: {content}" for speaker, content in rows]
        return "Here is the previous conversation record:\n" + "\n".join(history_lines) + "\n\n"

    def get_active_client(self):
        if not self.clients:
            return None, None
        return self.clients[self.current_index]

    def rotate_to_next_client(self):
        """Switch to next API Key"""
        if not self.clients:
            return False
        old_name, _ = self.clients[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.clients)
        new_name, _ = self.clients[self.current_index]
        print(f"[SWITCH] [Multi-Key System] Quota reached, switching from {old_name} to {new_name}", flush=True)
        return self.current_index == 0

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 1. Strictly prevent bot from responding to "itself"
        if message.author == self.bot.user:
            return

        # 2. Check if @ mentioned, or if message is a Reply to the bot
        is_mentioned = self.bot.user in message.mentions
        is_reply_to_bot = False

        if message.reference and message.reference.resolved:
            replied_message = message.reference.resolved
            if replied_message.author == self.bot.user:
                is_reply_to_bot = True

        if not is_mentioned and not is_reply_to_bot:
            return

        if not self.clients:
            await message.reply("[ERROR] AI client not initialized, please check Render environment variables (GEMINI_API_KEY2 to 11)!")
            return

        channel_id = message.channel.id

        # 3. 🛡️ Bot conversation "anti-infinite ping-pong loop" mechanism
        if message.author.bot:
            now = time.time()
            tracker = self.bot_interaction_tracker.get(channel_id, {"count": 0, "last_time": 0})

            if now - tracker["last_time"] > 30:
                tracker["count"] = 0

            tracker["count"] += 1
            tracker["last_time"] = now
            self.bot_interaction_tracker[channel_id] = tracker

            if tracker["count"] > 5:
                print(f"[STOP] [Channel {channel_id}] Detected bot continuous conversation reached 5 limit, activating protection pause.", flush=True)
                return

        async with message.channel.typing():
            try:
                clean_content = message.content.replace(f"<@!{self.bot.user.id}>", "").replace(f"<@{self.bot.user.id}>", "").strip()
                
                # -------------------------------------------------------------------
                # [ROLE] Chat persona setting feature: Check if there are persona setting command keywords
                # -------------------------------------------------------------------
                setting_prefixes = ["!setpersona", "setpersona:", "[setpersona]", "!setpersona"]
                matched_prefix = next((p for p in setting_prefixes if clean_content.startswith(p)), None)

                if matched_prefix:
                    # Extract content after the keyword as new persona
                    new_persona_text = clean_content[len(matched_prefix):].strip()
                    if new_persona_text:
                        self.set_persona(new_persona_text)
                        await message.reply(f"[OK] **[Identity Set Successfully]** New AI personality written to permanent database!\n\n[INFO] **Current Identity:**\n>>> {new_persona_text}")
                        return
                    else:
                        current_p = self.get_persona()
                        await message.reply(f"[INFO] **[Current AI Identity]:**\n>>> {current_p}\n\n[TIP] *To set identity in chat, use `@bot !setpersona your personality and background description`*")
                        return

                # Normal conversation processing
                if not clean_content and message.attachments:
                    clean_content = "Please help me look at this image or attachment."
                elif not clean_content:
                    clean_content = "Hello!"

                contents = []
                for attachment in message.attachments:
                    try:
                        file_bytes = await attachment.read()
                        mime = attachment.content_type or 'image/jpeg'
                        contents.append(types.Part.from_bytes(data=file_bytes, mime_type=mime))
                    except Exception as att_err:
                        print(f"Attachment read failed: {att_err}", flush=True)

                # [BRAIN] Load conversation history from SQLite
                history_prompt = self.load_chat_memory(channel_id, limit=8)

                # [IDEA] Discord Mention tag instructions
                sender_tag = f"<@{message.author.id}>"
                tag_instruction = f"[System Hint] You are conversing with '{message.author.display_name}' on Discord. If you need to @ mention them, include the tag: {sender_tag}\n\n"

                full_prompt = f"{tag_instruction}{history_prompt}User ({message.author.display_name}): {clean_content}"
                contents.append(full_prompt)

                # [ROLE] Dynamically load latest persona settings from database
                current_persona = self.get_persona()
                generation_config = types.GenerateContentConfig(
                    system_instruction=current_persona
                )

                response = None
                attempts = 0
                max_attempts = len(self.clients)

                while attempts < max_attempts:
                    key_name, client = self.get_active_client()
                    try:
                        response = await asyncio.to_thread(
                            client.models.generate_content,
                            model='gemini-2.5-flash',
                            contents=contents,
                            config=generation_config
                        )
                        break 
                    except ClientError as ce:
                        if ce.code == 429:
                            print(f"[WARNING] {key_name} triggered 429 quota limit", flush=True)
                            attempts += 1
                            if attempts >= max_attempts:
                                print("[ERROR] [Multi-Key System] All 10 API keys quota exhausted for today!", flush=True)
                                await message.reply("[WARNING] **[Quota Exhausted]** All 10 Gemini API free quotas have been used up today!")
                                return
                            self.rotate_to_next_client()
                            await asyncio.sleep(0.5)
                        else:
                            raise ce
                    except ServerError as se:
                        print(f"[WARNING] {key_name} triggered 503 server overload", flush=True)
                        attempts += 1
                        if attempts >= max_attempts:
                            await message.reply("[WARNING] AI servers currently overloaded, please try again later!")
                            return
                        await asyncio.sleep(1)

                if response and response.text:
                    reply_text = response.text
                    if len(reply_text) > 1900:
                        reply_text = reply_text[:1900] + "\n\n...(text too long, automatically truncated)"

                    # [DB] Write permanent conversation record
                    self.save_chat_memory(channel_id, f"User ({message.author.display_name})", clean_content)
                    self.save_chat_memory(channel_id, "AI", reply_text)

                    await message.reply(
                        reply_text,
                        mention_author=True,
                        allowed_mentions=discord.AllowedMentions(users=True, roles=False, replied_user=True)
                    )
                else:
                    await message.reply("[ERROR] AI currently has no response, please try again later.")

            except Exception as e:
                print(f"❌ Error processing mention conversation:", flush=True)
                traceback.print_exc()
                await message.reply(f"❌ Error occurred: `{e}`")

async def setup(bot):
    await bot.add_cog(AIMentionChat(bot))
