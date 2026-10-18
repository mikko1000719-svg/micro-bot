# Google Cloud Run 部署指南

## 🚀 部署到 Google Cloud Run

### 為什麼選 Cloud Run？
- ✅ 不同的 IP 區段（不受 Render 限制影響）
- ✅ 容器化部署（更穩定）
- ✅ 免費層（每月 $300 免費額度）
- ✅ 自動擴展
- ✅ 可以選擇部署地區

## 📋 部署步驟：

### 1. 準備 Google Cloud 帳號
- 訪問：https://console.cloud.google.com/
- 創建新專案
- 啟用 Cloud Run API

### 2. 安裝 Google Cloud SDK
下載並安裝：https://cloud.google.com/sdk/docs/install

### 3. 認證
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 4. 構建並部署

#### 方案 A：使用 gcloud（推薦）
```bash
cd micro-bot-main
gcloud run deploy weiguo-bot \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated
```

#### 方案 B：使用 Docker
```bash
# 構建 Docker 鏡像
docker build -t gcr.io/YOUR_PROJECT_ID/weiguo-bot .

# 推送到 Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/weiguo-bot

# 部署到 Cloud Run
gcloud run deploy weiguo-bot \
  --image gcr.io/YOUR_PROJECT_ID/weiguo-bot \
  --platform managed \
  --region asia-east1
```

### 5. 設置環境變量
在 Cloud Console 或使用 gcloud：
```bash
gcloud run services update weiguo-bot \
  --set-env-vars DISCORD_TOKEN=your_token \
  --set-env-vars GEMINI_API_KEY=your_key \
  --region asia-east1
```

## 🔧 Dockerfile 配置

項目已經包含 Dockerfile，可以直接使用。

## 📊 地區選擇：

推薦地區（避開可能的限制）：
- `asia-east1`（台灣）
- `asia-northeast1`（日本）
- `asia-southeast1`（新加坡）

## 💡 優點：

1. **IP 不同** - 不受 Render 限制
2. **穩定** - Google 基礎設施
3. **免費額度** - 每月 $300
4. **靈活** - 可以選擇地區

## ⚠️ 注意事項：

1. **需要 Google 帳號**
2. **需要綁定信用卡**（但不會扣費，除非超出免費額度）
3. **免費額度足夠機器人使用**

## 🎯 開始部署：

1. 去 Google Cloud Console
2. 創建專案
3. 啟用 Cloud Run API
4. 使用上面的命令部署

## 📝 Dockerfile（已存在）：

項目已經有 Dockerfile，可以直接用於 Cloud Run 部署。
