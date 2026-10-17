# Render 手動配置指南

## 🔧 在 Render Dashboard 手動設置

由於 render.yaml 和 Procfile 可能被緩存，建議直接在 Render Dashboard 設置：

### 步驟：

1. **打開 Render Dashboard**
   - 訪問你的服務設置頁面

2. **找到 "Build & Deploy" 部分**
   - 滾動到 "Build & Deploy" 設置

3. **設置 Build Command**
   ```
   python3 -m pip install --break-system-packages -r requirements.txt
   ```

4. **設置 Start Command**
   ```
   python3 main.py
   ```

5. **確保 Root Directory 是正確的**
   - 應該是空（使用倉庫根目錄）

6. **點擊 "Save Changes"**

7. **手動部署**
   - 點擊 "Manual Deploy"
   - 選擇 "Deploy latest commit"

## 🎯 為什麼這樣做？

- render.yaml 和 Procfile 可能被 Render 緩存
- 直接在 Dashboard 設置可以確保使用最新配置
- 避免文件衝突和緩存問題

## ⚠️ 注意事項：

- 確保使用 `python3` 而不是 `python`
- 確保使用 `--break-system-packages`
- 確保文件名是 `main.py` 不是 `bot.py`

## 📋 如果還是不行：

1. **刪除並重新創建服務**
   - 刪除現有的 Render 服務
   - 重新創建新服務
   - 從頭開始配置

2. **使用不同的服務名稱**
   - 有時候舊配置會被緩存
   - 使用新名稱可以避免這個問題
