# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session
import os
import json
import sqlite3
import time
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database file path
DB_FILE = "guild_settings.json"
AUTH_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "admin_auth.json")
WHITELIST_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "whitelist.json")
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "moderation_log.json")

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

    if guild_data['code'].upper() != code.upper():
        return False, f"驗證碼錯誤。正確的驗證碼是：{guild_data['code']}（請注意大小寫）"

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
    commands = [
        {"name": "ai", "description": "與 AI 進行對話", "category": "AI"},
        {"name": "cpbl", "description": "查看中職比賽比分", "category": "中職"},
        {"name": "ptt", "description": "PTP 棒球版連結", "category": "中職"},
        {"name": "ban", "description": "封禁用戶", "category": "管理"},
        {"name": "vckick", "description": "踢出語音頻道", "category": "管理"},
        {"name": "modlog", "description": "查看管理日誌", "category": "管理"},
        {"name": "whitelist_add", "description": "添加白名單", "category": "管理"},
        {"name": "whitelist_remove", "description": "移除白名單", "category": "管理"},
        {"name": "whitelist_list", "description": "查看白名單", "category": "管理"},
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

        is_valid, message = verify_auth_code(guild_id, code)

        if is_valid:
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

# Discord API integration endpoints (simplified)
@app.route('/api/discord/ban', methods=['POST'])
def discord_ban():
    """Ban a user via Discord API"""
    return jsonify({
        "success": False,
        "message": "Discord API 功能需要異步支持，目前建議在 Discord 中使用 /ban 指令"
    })

@app.route('/api/discord/kick', methods=['POST'])
def discord_kick():
    """Kick a user via Discord API"""
    return jsonify({
        "success": False,
        "message": "Discord API 功能需要異步支持，目前建議在 Discord 中使用 /vckick 指令"
    })

@app.route('/api/discord/mute', methods=['POST'])
def discord_mute():
    """Mute a user via Discord API"""
    return jsonify({
        "success": False,
        "message": "Discord API 功能需要異步支持，目前建議在 Discord 中使用 /mod_mute 指令"
    })

@app.route('/api/discord/whitelist_add', methods=['POST'])
def discord_whitelist_add():
    """Add user to whitelist"""
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

        # Load whitelist
        if os.path.exists(WHITELIST_FILE):
            with open(WHITELIST_FILE, 'r', encoding='utf-8') as f:
                whitelist = json.load(f)
        else:
            whitelist = {}

        guild_id_str = str(guild_id)
        if guild_id_str not in whitelist:
            whitelist[guild_id_str] = {}

        user_id_str = str(user_id)
        if user_id_str in whitelist[guild_id_str]:
            return jsonify({
                "success": False,
                "message": "用戶已在白名單中"
            })

        whitelist[guild_id_str][user_id_str] = {
            "reason": reason,
            "added_at": str(datetime.utcnow())
        }

        # Save whitelist
        with open(WHITELIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(whitelist, f, ensure_ascii=False, indent=4)

        return jsonify({
            "success": True,
            "message": f"已將用戶 {user_id} 添加到白名單"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"錯誤: {str(e)}"
        })

@app.route('/api/discord/whitelist_remove', methods=['POST'])
def discord_whitelist_remove():
    """Remove user from whitelist"""
    try:
        data = request.json
        user_id = data.get('user_id')
        guild_id = data.get('guild_id')

        if not user_id or not guild_id:
            return jsonify({
                "success": False,
                "message": "缺少 user_id 或 guild_id"
            })

        if not os.path.exists(WHITELIST_FILE):
            return jsonify({
                "success": False,
                "message": "白名單文件不存在"
            })

        with open(WHITELIST_FILE, 'r', encoding='utf-8') as f:
            whitelist = json.load(f)

        guild_id_str = str(guild_id)
        if guild_id_str not in whitelist:
            return jsonify({
                "success": False,
                "message": "該伺服器沒有白名單記錄"
            })

        user_id_str = str(user_id)
        if user_id_str not in whitelist[guild_id_str]:
            return jsonify({
                "success": False,
                "message": "用戶不在白名單中"
            })

        del whitelist[guild_id_str][user_id_str]

        # Save whitelist
        with open(WHITELIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(whitelist, f, ensure_ascii=False, indent=4)

        return jsonify({
            "success": True,
            "message": f"已將用戶 {user_id} 從白名單移除"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"錯誤: {str(e)}"
        })

@app.route('/api/discord/whitelist_list', methods=['GET'])
def discord_whitelist_list():
    """List whitelist users"""
    try:
        guild_id = request.args.get('guild_id')

        if not guild_id:
            return jsonify({
                "success": False,
                "message": "缺少 guild_id"
            })

        if not os.path.exists(WHITELIST_FILE):
            return jsonify({
                "success": True,
                "message": "白名單為空",
                "whitelist": []
            })

        with open(WHITELIST_FILE, 'r', encoding='utf-8') as f:
            whitelist = json.load(f)

        guild_id_str = str(guild_id)
        if guild_id_str not in whitelist or not whitelist[guild_id_str]:
            return jsonify({
                "success": True,
                "message": "白名單為空",
                "whitelist": []
            })

        return jsonify({
            "success": True,
            "message": f"共 {len(whitelist[guild_id_str])} 位用戶",
            "whitelist": whitelist[guild_id_str]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"錯誤: {str(e)}"
        })

@app.route('/api/discord/logs', methods=['GET'])
def discord_logs():
    """Get moderation logs"""
    try:
        guild_id = request.args.get('guild_id')
        limit = int(request.args.get('limit', 10))

        if not guild_id:
            return jsonify({
                "success": False,
                "message": "缺少 guild_id"
            })

        if not os.path.exists(LOG_FILE):
            return jsonify({
                "success": True,
                "message": "沒有管理日誌",
                "logs": []
            })

        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)

        guild_id_str = str(guild_id)
        if guild_id_str not in logs or not logs[guild_id_str]:
            return jsonify({
                "success": True,
                "message": "沒有管理日誌",
                "logs": []
            })

        recent_logs = logs[guild_id_str][-limit:]

        return jsonify({
            "success": True,
            "message": f"最近 {len(recent_logs)} 條日誌",
            "logs": recent_logs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"錯誤: {str(e)}"
        })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
