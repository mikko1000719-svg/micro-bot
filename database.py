import json
import os

DB_FILE = "guild_settings.json"

def load_all_settings():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_all_settings(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_guild_config(guild_id: str):
    data = load_all_settings()
    # 預設各伺服器的防炸群設定
    default_config = {
        "anti_spam_enabled": True,
        "time_window": 10.0,
        "max_messages": 6,
        "mute_hours": 3
    }
    return data.get(str(guild_id), default_config)

def update_guild_config(guild_id: str, new_config: dict):
    data = load_all_settings()
    data[str(guild_id)] = new_config
    save_all_settings(data)