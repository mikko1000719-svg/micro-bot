#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動化部署腳本 - Koyeb 部署
可以自動配置環境變量並部署機器人
"""

import os
import subprocess
import json
import time

def load_env_file():
    """從 .env 文件加載環境變量"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print("⚠️  .env 文件不存在")
    return env_vars

def create_koyeb_config():
    """創建 Koyeb 部署配置"""
    config = {
        "name": "weiguo-bot",
        "env_vars": load_env_file(),
        "region": "sgp1",  # 新加坡
        "instance_type": "nano"
    }
    return config

def deploy_to_koyeb():
    """部署到 Koyeb"""
    print("🚀 開始部署到 Koyeb...")

    # 檢查是否安裝 koyeb CLI
    try:
        result = subprocess.run(['koyeb', '--version'], capture_output=True, text=True)
        print(f"✅ Koyeb CLI 已安裝: {result.stdout}")
    except FileNotFoundError:
        print("❌ Koyeb CLI 未安裝")
        print("請運行: pip install koyeb")
        return False

    # 創建配置
    config = create_koyeb_config()
    print(f"📋 配置: {config}")

    # 部署命令（需要 koyeb CLI 支持）
    print("📝 注意: 需要手動在 Koyeb Dashboard 設置 API Token")
    print("📝 然後運行: koyeb deploy")

    return True

if __name__ == "__main__":
    deploy_to_koyeb()
