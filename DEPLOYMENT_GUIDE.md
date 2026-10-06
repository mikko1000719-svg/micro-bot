# 微國機器人網站部署指南

## 🚀 部署到 Render

### 方案 1：創建新的 Web Service（推薦）

1. **登入 Render Dashboard**
   - 去 https://dashboard.render.com/

2. **創建新的 Web Service**
   - 點擊 "New +"
   - 選擇 "Web Service"
   - 連接到 GitHub 倉庫：`mikko1000719-svg/micro-bot`

3. **配置設置**
   - **Name**: `micro-bot-website`
   - **Root Directory**: `website`
   - **Plan**: Free
   - Build Command 和 Start Command：留空（Render 會自動檢測）

4. **環境變量**
   - `SECRET_KEY`：點擊 "Generate" 生成隨機密鑰（已自動配置）

5. **部署**
   - 點擊 "Create Web Service"
   - 等待部署完成（約 2-3 分鐘）

### 方案 2：使用其他免費平台

#### Vercel
1. 安裝 Vercel CLI: `npm i -g vercel`
2. 在 `website/` 文件夾運行: `vercel`
3. 按照提示完成部署

#### Netlify
1. 登入 Netlify
2. 拖拽 `website/` 文件夾到 Netlify
3. 自動部署

## 📋 部署後的配置

### 獲取網站 URL
- 部署完成後，Render 會提供網站 URL
- 格式：`https://micro-bot-website.onrender.com`

### 更新機器人配置
- 如果需要，更新機器人中的網站連結
- 確保驗證碼文件路徑正確

## 🔧 故障排除

### 部署失敗
- 檢查 build 日誌
- 確認 Python 版本正確
- 檢查依賴包是否正確安裝

### 驗證碼無法工作
- 確認 `admin_auth.json` 文件路徑正確
- 檢查機器人和網站是否在同一個伺服器
- 確認文件權限正確

## 🎯 部署後測試

1. 測試網站是否正常訪問
2. 測試管理面板登入功能
3. 測試驗證碼系統
