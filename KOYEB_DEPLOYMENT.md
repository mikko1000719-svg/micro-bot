# Koyeb 部署指南

## 🚀 部署到 Koyeb

### 為什麼選 Koyeb？
- ✅ 不同的 IP 區段（不受 Render 限制影響）
- ✅ 容器化部署（使用 Docker）
- ✅ 免費層（$5.50/月免費額度）
- ✅ 全球部署地區選擇
- ✅ 從 GitHub 直接部署
- ✅ 自動 HTTPS

## 📋 部署步驟：

### 1. 註冊 Koyeb
- 訪問：https://app.koyeb.com
- 使用 GitHub 帳號登入

### 2. 創建新服務
- 點擊 "Create Service"
- 選擇 "GitHub"
- 輸入倉庫：`mikko1000719-svg/micro-bot`

### 3. 配置部署設置

#### 基本設置：
- **Name**: `weiguo-bot`
- **Region**: 選擇地區（建議離台灣近的）
  - `sgp1`（新加坡）
  - `par1`（巴黎）
  - `was1`（華盛頓）

#### 構建設置：
- **Build Method**: Dockerfile
- **Dockerfile**: `Dockerfile`（根目錄）
- **Context**: `/`（根目錄）

#### 環境變量：
- `DISCORD_TOKEN`: 你的機器人 Token
- `GEMINI_API_KEY`: 你的 Gemini API Key
- `GEMINI_API_KEY2`: 第二個 Gemini API Key

### 4. 部署
- 點擊 "Deploy"
- 等待部署完成

### 5. 查看日誌
- 部署完成後點擊服務
- 查看 "Logs" 標籤
- 確認機器人成功上線

## 🔧 Dockerfile 配置

項目已經包含 Dockerfile，可以直接使用。

## 📊 地區選擇：

推薦地區（避免限制）：
- `sgp1`（新加坡）- 亞洲
- `par1`（巴黎）- 歐洲
- `was1`（華盛頓）- 美國

## 💡 Koyeb 免費層：

- **免費額度**: $5.50/月
- **足夠機器人使用**
- **自動停止**：超出額度後停止

## 🎯 開始部署：

1. 去 https://app.koyeb.com
2. 登入並創建新服務
3. 連接到 GitHub 倉庫
4. 設置環境變量
5. 部署！

## 📝 優點：

1. **IP 不同** - 不受 Render 限制
2. **簡單** - GitHub 直接部署
3. **穩定** - 全球基礎設施
4. **免費** - 有免費額度

## ⚠️ 注意事項：

1. **需要 GitHub 帳號**
2. **免費額度有限** - 但足夠機器人
3. **超出額度會停止** - 但不會扣費
