# Railway 部署指南

## 🚀 部署到 Railway（解決 IP 限制問題）

### 為什麼選 Railway？
- ✅ Railway 使用不同的 IP 區段
- ✅ 不受 Render 的 Cloudflare 限制影響
- ✅ 免費計劃
- ✅ 自動部署
- ✅ 支持環境變量

## 📋 �署步驟：

### 1. 註冊 Railway
- 註冊：https://railway.app/
- 使用 GitHub 帳號登入

### 2. 創建新專案
- 點擊 "New Project"
- 選擇 "Deploy from GitHub repo"
- 輸入倉庫：`mikko1000719-svg/micro-bot`

### 3. 配置環境變量
在 Railway 設置頁面添加：
- `DISCORD_TOKEN` - 你的 Discord 機器人 Token
- `GEMINI_API_KEY` - 你的 Gemini API Key
- `GEMINI_API_KEY2` - 第二個 Gemini API Key
- （其他需要的環境變量）

### 4. 部署
- 點擊 "Deploy"
- 等待部署完成

### 5. 查看日誌
- 點擊 "View Logs"
- 查看機器人是否成功上線

## 🔧 配置文件說明：

項目已經包含所有必要的配置文件：
- `main.py` - 機器人主程序
- `requirements.txt` - Python 依賴
- `Procfile` - Railway 會自動檢測

## 📋 網站部署：

### 選項 1：使用 Railway（與機器人一起）
- 可以在同一個 Railway 專案中
- 使用 Railway 的網站功能

### 選項 2：使用 GitHub Pages（網站單獨）
- 已經配置好 GitHub Pages
- 文件在 `docs/` 文件夾
- 完全免費

## ⚠️ 注意事項：

1. **環境變量** - Railway 需要設置所有環境變量
2. **免費限制** - Railway 免費計劃有使用限制
3. **休眠** - 無活動會休眠（但機器人會自動重連）

## 🎯 建議：

1. **先部署機器人到 Railway**
2. **確認機器人成功上線**
3. **再決定網站部署方式**

## 📊 Railway vs Render 對比：

| 功能 | Railway | Render |
|------|---------|--------|
| IP 區段 | 不同 | 固定 |
| 免費計劃 | ✅ | ✅ |
| 休眠 | 無活動休眠 | 無活動休眠 |
| 環境變量 | ✅ | ✅ |
| 自動部署 | ✅ | ✅ |
| Cloudflare 限制 | 可能沒有 | 有 |

## 🚀 開始部署：

1. 去 https://railway.app/
2. 登入並創建新專案
3. 連接到 GitHub 倉庫
4. 設置環境變量
5. 部署！

## 💡 備 Railway 上線後：

機器人應該能夠：
- ✅ 成功連接到 Discord
- ✅ 避免 Cloudflare 429 錯誤
- ✅ 正常運行所有功能
