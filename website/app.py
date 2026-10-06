# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session
import os
import json
import sqlite3
import time
from functools import wraps

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database file path
DB_FILE = "guild_settings.json"
AUTH_FILE = "../admin_auth.json"

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
    # For now, return a static list
    commands = [
        {"name": "ai", "description": "與 AI 進行對話", "category": "AI"},
        {"name": "gomoku", "description": "玩五子棋", "category": "遊戲"},
        {"name": "play_balloon", "description": "玩氣球遊戲", "category": "遊戲"},
        {"name": "play_coinflip", "description": "拋硬幣", "category": "遊戲"},
        {"name": "play_dice", "description": "擲骰子", "category": "遊戲"},
        {"name": "linkgroup", "description": "加入跨服群組", "category": "跨服"},
        {"name": "unlinkgroup", "description": "退出跨服群組", "category": "跨服"},
        {"name": "mod_ban", "description": "封禁用戶", "category": "管理"},
        {"name": "mod_kick", "description": "踢出用戶", "category": "管理"},
        {"name": "mod_mute", "description": "禁言用戶", "category": "管理"},
        {"name": "play", "description": "播放音樂", "category": "音樂"},
        {"name": "pause", "description": "暫停音樂", "category": "音樂"},
        {"name": "skip", "description": "跳過當前歌曲", "category": "音樂"},
        {"name": "stop", "description": "停止音樂", "category": "音樂"},
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
