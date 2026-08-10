import os
import asyncio
import threading
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
from flask import Flask

# 設定系統日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 建立 Flask 伺服器供雲端健康檢查使用
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Bot is online and active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    try:
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        logging.error(f"Flask 伺服器啟動例外: {e}")

# 初始化 Discord Bot 權限
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True  # 啟用音樂語音頻道權限

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    logging.info(f"🤖 機器人已成功上線！登入名稱：{bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        logging.info(f"✅ 成功同步 {len(synced)} 個斜線指令！")
    except Exception as e:
        logging.error(f"❌ 斜線指令同步失敗: {e}")

async def load_cogs():
    cog_folder = "./cogs"
    if os.path.exists(cog_folder):
        for filename in os.listdir(cog_folder):
            if filename.endswith(".py") and not filename.startswith("__"):
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await bot.load_extension(cog_name)
                    logging.info(f"🟢 成功載入模組: {filename}")
                except Exception as e:
                    logging.error(f"🔴 載入模組 {filename} 失敗: {e}")

async def main():
    async with bot:
        await load_cogs()
        
        if not TOKEN:
            logging.error("❌ 致命錯誤：環境變數中找不到 DISCORD_TOKEN！")
            return

        try:
            await bot.start(TOKEN, reconnect=True)
        except Exception as e:
            logging.error(f"❌ 連線發生未預期例外: {e}")

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("機器人手動關閉。")
    except Exception as e:
        logging.error(f"❌ 主行程例外崩潰: {e}")