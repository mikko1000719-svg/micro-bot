# 微國機器人 5.0 - 部署指南

## ✅ 已完成的改進

### 1. **中職比賽顯示改進**
- ✅ 添加了記分板風格的顯示
- ✅ 包含局數比分（1-9 局）
- ✅ 顯示總分（R）、安打（H）、失誤（E）
- ✅ 改進視覺呈現

### 2. **指令重命名（基於功能）**
- ✅ `mod_ban` → `ban` （封禁用戶）
- ✅ `mod_vckick` → `vckick` （踢出語音頻道）
- ✅ 改進了中文描述

### 3. **新增管理指令**
- ✅ `ban` - 封禁用戶
- ✅ `vckick` - 踢出語音頻道
- ✅ `modlog` - 查看管理日誌
- ✅ `whitelist_add` - 添加白名單
- ✅ `whitelist_remove` - 移除白名單
- ✅ `whitelist_list` - 查看白名單

### 4. **網站改進**
- ✅ 添加了 40+ 個指令到官網
- ✅ 按類別組織（AI、遊戲、跨服、管理、音樂、中職）
- ✅ 完整的指令列表

### 5. **配置簡化**
- ✅ 簡化了 Render 配置
- ✅ 自動檢測 Python 版本
- ✅ 自動安裝依賴

## 🚀 部署到 Render

### 機器人部署

1. **去 Render Dashboard**
   - 訪問 https://dashboard.render.com/

2. **檢查現有服務**
   - 你的機器人服務應該已經存在
   - 名稱：`weiguo-bot`

3. **手動部署**
   - 點擊 "Manual Deploy"
   - 選擇 "Deploy latest commit"
   - 等待部署完成

### 網站部署

1. **創建新的 Web Service**
   - 點擊 "New +"
   - 選擇 "Web Service"
   - 連接到 GitHub 倉庫

2. **配置設置**
   - **Name**: `micro-bot-website`
   - **Root Directory**: `website`
   - **Plan**: Free
   - Build Command 和 Start Command：留空

3. **環境變量**
   - `SECRET_KEY`：點擊 "Generate" 自動生成

4. **部署**
   - 點擊 "Create Web Service"
   - 等待部署完成

## 📋 新增指令說明

### 管理指令

#### `/ban`
- **功能**: 封禁用戶
- **權限**: 管理員
- **用法**: `/ban @用戶 [原因]`

#### `/vckick`
- **功能**: 踢出語音頻道
- **權限**: 管理員
- **用法**: `/vckick @用戶`

#### `/modlog`
- **功能**: 查看管理日誌
- **權限**: 管理員
- **用法**: `/modlog [數量]`

#### `/whitelist_add`
- **功能**: 添加白名單
- **權限**: 管理員
- **用法**: `/whitelist_add @用戶 [原因]`

#### `/whitelist_remove`
- **功能**: 移除白名單
- **權限**: 管理員
- **用法**: `/whitelist_remove @用戶`

#### `/whitelist_list`
- **功能**: 查看白名單
- **權限**: 管理員
- **用法**: `/whitelist_list`

### 中職指令

#### `/cpbl`
- **功能**: 查看中職比賽比分
- **顯示**: 記分板風格，包含局數比分

#### `/ptt`
- **功能**: PTP 棒球版連結
- **顯示**: PTP 棒球版連結

## 🎯 注意事項

### 關於 Cloudflare 限制
- Render IP 可能仍被 Cloudflare 限制
- 建議等待幾小時讓限制自動解除
- 避免頻繁重新部署

### 關於環境變量
- 確保 Render 中設置了正確的環境變量
- DISCORD_TOKEN
- GEMINI_API_KEY
- SECRET_KEY（網站）

### 關於網站
- 網站需要單獨部署到 Render
- 網站和機器人使用不同的服務
- 網站需要 SECRET_KEY 環境變量

## 📊 統計

- **總模組數**: 88 個
- **總指令數**: 93 個
- **網站指令數**: 40+ 個
- **新增管理指令**: 6 個

## 🎉 完成狀態

所有任務已完成：
- ✅ 重命名指令代碼
- ✅ 改進中職比賽顯示
- ✅ 修復掛掉的程序
- ✅ 把所有指令放上官網
- ✅ 添加管理指令
- ✅ 準備雲端部署

現在可以部署到 Render 了！
