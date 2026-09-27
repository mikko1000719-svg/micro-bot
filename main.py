# -*- coding: utf-8 -*-
import os
import discord
from discord.ext import commands
import keep_alive  # Import background keep-alive mechanism
from dotenv import load_dotenv  # Import dotenv to load .env file

# Load .env file
load_dotenv()

# -------------------------------------------------------------
# [SETTING] Configuration Area (Adjust as needed)
# -------------------------------------------------------------
# If you want 99+ commands to appear "instantly" in a specific server, paste your Discord server ID (number)
# If left as None, global sync will be executed (takes about 1 hour to display completely in Discord)
TEST_GUILD_ID = None  # Example: TEST_GUILD_ID = 123456789012345678
# TODO: Replace None with your Discord server ID for instant sync: TEST_GUILD_ID = YOUR_SERVER_ID

class MicroBot(commands.Bot):
    def __init__(self):
        # Set bot complete Intents permissions
        intents = discord.Intents.default()
        intents.message_content = True  # Allow reading messages
        intents.members = True          # Allow reading members

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        print("==========================================")
        print("[System] Starting recursive scan of all 99+ command modules in cogs/ folder...")

        cogs_dir = "./cogs"
        loaded_count = 0
        failed_count = 0

        if os.path.exists(cogs_dir):
            # Use os.walk to recursively search all subfolders (e.g., cogs/ai/, cogs/tools/)
            for root, _, files in os.walk(cogs_dir):
                for filename in files:
                    if filename.endswith(".py") and not filename.startswith("__"):
                        # Convert file path to Python module format (e.g., cogs.ai.chat_bot)
                        filepath = os.path.join(root, filename)
                        rel_path = os.path.relpath(filepath, ".")
                        module_name = rel_path.replace(os.sep, ".")[:-3]

                        try:
                            await self.load_extension(module_name)
                            print(f"  - [OK] Successfully loaded module: {module_name}", flush=True)
                            loaded_count += 1
                        except Exception as e:
                            print(f"  - [ERROR] Loading failed [{module_name}]: {e}", flush=True)
                            import traceback
                            traceback.print_exc()
                            failed_count += 1
        else:
            print("[WARNING] cogs folder not found, please check directory structure!")

        print(f"[System] Module loading complete: {loaded_count} successful, {failed_count} failed.")
        print("==========================================")

        # Execute slash command tree sync
        print("[System] Syncing slash commands to Discord...", flush=True)
        try:
            if TEST_GUILD_ID:
                # Server-specific sync (instant effect)
                print(f"[DEBUG] Using server-specific sync with guild ID: {TEST_GUILD_ID}", flush=True)
                guild = discord.Object(id=TEST_GUILD_ID)
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                print(f"[OK] [Instant Sync] Synced {len(synced)} slash commands to specified server ({TEST_GUILD_ID})!", flush=True)
            else:
                # Global sync (takes effect across Discord, requires about 1 hour)
                print("[DEBUG] Using global sync (may take up to 1 hour to appear)", flush=True)
                synced = await self.tree.sync()
                print(f"[OK] [Global Sync] Global sync request sent! Synced {len(synced)} slash commands (global effect takes about 1 hour).", flush=True)
        except Exception as e:
            print(f"[ERROR] Error during slash command sync: {e}", flush=True)
            import traceback
            traceback.print_exc()

    async def on_ready(self):
        print("==========================================")
        print(f"[BOT] Bot successfully online!")
        print(f"Account: {self.user.name} (ID: {self.user.id})")
        print("==========================================")

# Create Bot instance
bot = MicroBot()

# Start background Web Server to prevent sleep on Render platform
keep_alive.keep_alive()

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        import time
        from discord.errors import HTTPException

        # Add delay to avoid rate limiting
        print("[System] Waiting 30 seconds before Discord login to avoid rate limiting...")
        time.sleep(30)

        max_retries = 3
        retry_delay = 120  # 2 minutes between retries

        for attempt in range(max_retries):
            try:
                bot.run(TOKEN)
                break
            except HTTPException as e:
                if e.status == 429:
                    print(f"[WARNING] Rate limited by Discord. Attempt {attempt + 1}/{max_retries}. Waiting {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"[ERROR] Discord login error: {e}")
                    raise
            except Exception as e:
                print(f"[ERROR] Unexpected error: {e}")
                import traceback
                traceback.print_exc()
                raise
    else:
        print("[ERROR] DISCORD_TOKEN environment variable not found!")
