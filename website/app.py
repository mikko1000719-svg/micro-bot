# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session
import os
import json
import sqlite3
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database file path
DB_FILE = "guild_settings.json"
AUTH_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "admin_auth.json")

# Discord API integration
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
if DISCORD_TOKEN:
    # Initialize Discord client for API calls
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    discord_client = discord.Client(intents=intents)
else:
    discord_client = None

def load_settings():
    """Load guild settings from JSON file"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_settings(data):
    """Save guild settings to JSON file"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_auth_data():
    """Load auth codes from file"""
    try:
        if os.path.exists(AUTH_FILE):
            with open(AUTH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        return {}
    return {}

def verify_auth_code(guild_id, code):
    """Verify admin auth code"""
    data = load_auth_data()
    guild_data = data.get(str(guild_id))

    if not guild_data:
        return False, "驗證碼不存在，請先在 Discord 中使用 !generate_admin_code 生成"

    # Check if code matches (case-insensitive)
    if guild_data['code'].upper() != code.upper():
        return False, f"驗證碼錯誤。正確的驗證碼是：{guild_data['code']}（請注意大小寫）"

    # Check if code is expired (5 minutes)
    current_time = time.time()
    if current_time - guild_data['timestamp'] > 300:
        return False, "驗證碼已過期，請重新生成"

    return True, "驗證成功"

def get_guild_config(guild_id):
    """Get configuration for a specific guild"""
    data = load_settings()
    default_config = {
        "anti_spam_enabled": True,
        "time_window": 10.0,
        "max_messages": 6,
        "mute_hours": 3
    }
    return data.get(str(guild_id), default_config)

def update_guild_config(guild_id, new_config):
    """Update configuration for a specific guild"""
    data = load_settings()
    data[str(guild_id)] = new_config
    save_settings(data)

# Routes
@app.route('/')
def index():
    """Serve the main website"""
    return render_template('index.html')

@app.route('/api/guild/<guild_id>', methods=['GET'])
def get_guild_settings(guild_id):
    """API endpoint to get guild settings"""
    config = get_guild_config(guild_id)
    return jsonify({
        "success": True,
        "config": config
    })

@app.route('/api/guild/<guild_id>', methods=['POST'])
def update_guild_settings(guild_id):
    """API endpoint to update guild settings"""
    try:
        new_config = request.json
        update_guild_config(guild_id, new_config)
        return jsonify({
            "success": True,
            "message": "設定已更新"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"更新失敗: {str(e)}"
        }), 400

@app.route('/api/guilds', methods=['GET'])
def list_guilds():
    """API endpoint to list all guilds"""
    data = load_settings()
    guilds = []
    for guild_id, config in data.items():
        guilds.append({
            "guild_id": guild_id,
            "anti_spam_enabled": config.get("anti_spam_enabled", False),
            "time_window": config.get("time_window", 10.0),
            "max_messages": config.get("max_messages", 6),
            "mute_hours": config.get("mute_hours", 3)
        })
    return jsonify({
        "success": True,
        "guilds": guilds
    })

@app.route('/api/commands', methods=['GET'])
def list_commands():
    """API endpoint to list all commands"""
    # This would normally be fetched from the bot dynamically
    # For now, return a comprehensive list
    commands = [
        # AI 功能
        {"name": "ai", "description": "與 AI 進行對話", "category": "AI"},

        # 遊戲
        {"name": "gomoku", "description": "玩五子棋", "category": "遊戲"},
        {"name": "play_balloon", "description": "玩氣球遊戲", "category": "遊戲"},
        {"name": "play_coinflip", "description": "拋硬幣", "category": "遊戲"},
        {"name": "play_dice", "description": "擲骰子", "category": "遊戲"},
        {"name": "play_card_duel", "description": "卡牌決鬥", "category": "遊戲"},
        {"name": "play_destiny_wheel", "description": "命運輪盤", "category": "遊戲"},
        {"name": "play_draw", "description": "抽卡", "category": "遊戲"},
        {"name": "play_fist_wheel", "description": "拳頭輪盤", "category": "遊戲"},
        {"name": "play_fortune", "description": "占卜", "category": "遊戲"},
        {"name": "play_gacha", "description": "扭蛋", "category": "遊戲"},
        {"name": "play_ghost_card", "description": "鬼牌", "category": "遊戲"},
        {"name": "play_lottery", "description": "彩票", "category": "遊戲"},
        {"name": "play_lucky", "description": "幸運抽獎", "category": "遊戲"},
        {"name": "play_number_war", "description": "數字戰爭", "category": "遊戲"},
        {"name": "play_password", "description": "密碼遊戲", "category": "遊戲"},
        {"name": "play_poke", "description": "戳戳樂", "category": "遊戲"},
        {"name": "play_range_guess", "description": "範圍猜測", "category": "遊戲"},
        {"name": "play_reaction", "description": "反應遊戲", "category": "遊戲"},
        {"name": "play_roulette", "description": "輪盤賭", "category": "遊戲"},
        {"name": "play_rps", "description": "猜拳", "category": "遊戲"},
        {"name": "play_super_wheel", "description": "超級輪盤", "category": "遊戲"},
        {"name": "play_tictactoe", "description": "井字棋", "category": "遊戲"},
        {"name": "play_vault", "description": "保險箱", "category": "遊戲"},
        {"name": "play_wheel", "description": "輪盤", "category": "遊戲"},

        # 跨服
        {"name": "linkgroup", "description": "加入跨服群組", "category": "跨服"},
        {"name": "unlinkgroup", "description": "退出跨服群組", "category": "跨服"},

        # 管理
        {"name": "ban", "description": "封禁用戶", "category": "管理"},
        {"name": "vckick", "description": "踢出語音頻道", "category": "管理"},
        {"name": "modlog", "description": "查看管理日誌", "category": "管理"},
        {"name": "whitelist_add", "description": "添加白名單", "category": "管理"},
        {"name": "whitelist_remove", "description": "移除白名單", "category": "管理"},
        {"name": "whitelist_list", "description": "查看白名單", "category": "管理"},

        # 音樂
        {"name": "play", "description": "播放音樂", "category": "音樂"},
        {"name": "pause", "description": "暫停音樂", "category": "音樂"},
        {"name": "skip", "description": "跳過當前歌曲", "category": "音樂"},
        {"name": "stop", "description": "停止音樂", "category": "音樂"},

        # 中職
        {"name": "cpbl", "description": "查看中職比賽比分", "category": "中職"},
        {"name": "ptt", "description": "PTP 棒球版連結", "category": "中職"},

        # 其他
        {"name": "cpbl", "description": "查看中職比賽比分", "category": "資訊"},
        {"name": "announce", "description": "發送公告", "category": "資訊"},
        {"name": "stock_market", "description": "股票市場", "category": "資訊"},
        {"name": "serverinfo", "description": "伺服器資訊", "category": "資訊"},
    ]
    return jsonify({
        "success": True,
        "commands": commands
    })

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """API endpoint for admin login with verification code"""
    try:
        data = request.json
        guild_id = data.get('guild_id')
        code = data.get('code')

        if not guild_id or not code:
            return jsonify({
                "success": False,
                "message": "請提供伺服器 ID 和驗證碼"
            }), 400

        # Verify the auth code
        is_valid, message = verify_auth_code(guild_id, code)

        if is_valid:
            # Store guild_id in session
            session['guild_id'] = guild_id
            session['authenticated'] = True

            return jsonify({
                "success": True,
                "message": "登入成功",
                "guild_id": guild_id
            })
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"登入失敗: {str(e)}"
        }), 500

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """API endpoint for admin logout"""
    session.clear()
    return jsonify({
        "success": True,
        "message": "已登出"
    })

# Discord API integration endpoints
@app.route('/api/discord/ban', methods=['POST'])
async def discord_ban():
    """Ban a user via Discord API"""
    if not DISCORD_TOKEN:
        return jsonify({
            "success": False,
            "message": "未設置 DISCORD_TOKEN 環境變量"
        })

    try:
        data = request.json
        user_id = data.get('user_id')
        reason = data.get('reason', '')
        guild_id = data.get('guild_id')

        if not user_id or not guild_id:
            return jsonify({
                "success": False,
                "message": "缺少 user_id 或 guild_id"
            })

        # Use Discord REST API to ban user
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bot {DISCORD_TOKEN}',
                'Content-Type': 'application/json'
            }

            url = f'https://discord.com/api/v10/guilds/{guild_id}/bans/{user_id}'
            payload = {'reason': reason}

            async with session.put(url, json=payload, headers=headers) as response:
                if response.status == 204:
                    return jsonify({
                        "success": True,
                        "message": f"已封禁用戶 {user_id}"
                    })
                else:
                    error_text = await response.text()
                    return jsonify({
                        "success": False,
                        "message": f"封禁失敗: {error_text}"
                    })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"錯誤: {str(e)}"
        })

@app.route('/api/discord/kick', methods=['POST'])
async def discord_kick():
    """Kick a user via Discord API"""
    if not DISCORD_TOKEN:
        return jsonify({
            "success": False,
            "message": "未設置 DISCORD_TOKEN 環境變量"
        })

    try:
        data = request.json
        user_id = data.get('user_id')
        reason = data.get('reason', '')
        guild_id = data.get('guild_id')

        if not user_id or not guild_id:
            return jsonify({
                "success": False,
                "message": "缺少 user_id 或 guild_id"
            })

        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bot {DISCORD_TOKEN}',
                'Content-Type': 'application/json'
            }

            url = f'https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}'
            payload = {'reason': reason}

            async with session.delete(url, json=payload, headers=headers) as response:
                if response.status == 204:
                    return jsonify({
                        "success": True,
                        "message": f"已踢出用戶 {user_id}"
                    })
                else:
                    error_text = await response.text()
                    return jsonify({
                        "success": False,
                        "message": f"踢出失敗: {error_text}"
                    })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"錯誤: {str(e)}"
        })

@app.route('/api/discord/mute', methods=['POST'])
async def discord_mute():
    """Mute a user via Discord API"""
    if not DISCORD_TOKEN:
        return jsonify({
            "success": False,
            "message": "未設置 DISCORD_TOKEN 環境變量"
        })

    try:
        data = request.json
        user_id = data.get('user_id')
        reason = data.get('reason', '')
        guild_id = data.get('guild_id')
        mute_duration = data.get('duration', 3600)  # Default 1 hour

        if not user_id or not guild_id:
            return jsonify({
                "success": False,
                "message": "缺少 user_id 或 guild_id"
            })

        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bot {DISCORD_TOKEN}',
                'Content-Type': 'application/json'
            }

            # Get current timeout and add duration
            url = f'https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}'
            payload = {
                'communication_disabled_until': str(datetime.utcnow() + timedelta(seconds=mute_duration))
            }

            async with session.patch(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    return jsonify({
                        "success": True,
                        "message": f"已禁言用戶 {user_id}"
                    })
                else:
                    error_text = await response.text()
                    return jsonify({
                        "success": False,
                        "message": f"禁言失敗: {error_text}"
                    })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"錯誤: {str(e)}"
        })

@app.route('/api/discord/whitelist_add', methods=['POST'])
def discord_whitelist_add():
    """Add user to whitelist"""
    # This can use the local whitelist file
    data = request.json
    # TODO: Implement whitelist management
    return jsonify({
        "success": False,
        "message": "此功能需要完整實現。"
    })

@app.route('/api/discord/whitelist_remove', methods=['POST'])
def discord_whitelist_remove():
    """Remove user from whitelist"""
    return jsonify({
        "success": False,
        "message": "此功能需要完整實現。"
    })

@app.route('/api/discord/whitelist_list', methods=['GET'])
def discord_whitelist_list():
    """List whitelist users"""
    return jsonify({
        "success": False,
        "message": "此功能需要完整實現。"
    })

@app.route('/api/discord/logs', methods=['GET'])
def discord_logs():
    """Get moderation logs"""
    # This can use the local log file
    # TODO: Implement log reading
    return jsonify({
        "success": False,
        "message": "此功能需要完整實現。"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
