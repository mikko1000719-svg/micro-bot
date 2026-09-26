import os
from flask import Flask
from threading import Thread

# 建立 Flask 應用程式
app = Flask(__name__)

@app.route('/')
def home():
    """提供 Render 健康檢查回應的首頁"""
    return "🟢 微國機器人 5.0 運行中！", 200

def run():
    # 讀取 Render 自動分配的 PORT 環境變數，若無則預設為 10000
    port = int(os.environ.get("PORT", 10000))
    # 綁定 0.0.0.0 以接收外部網路請求
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    """使用獨立執行緒啟動 Flask 伺服器，避免阻塞 Discord 機器人"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
