# 🎬 電影AI助手聊天機器人

一個功能豐富的多模態聊天機器人，整合了電影相關的AI服務，包括智能對話、電影搜尋、圖片識別和字幕翻譯等功能。

## 靜態HTML Demo(前端畫面)
**Demo 網址**: [https://tsz7250.github.io/1131_Chatbot_Final/](https://tsz7250.github.io/1131_Chatbot_Final/)
<img src="./pic/index.png" alt="主頁">
<img src="./pic/translate.png" alt="字幕翻譯">


## ✨ 功能特色

### 🤖 四大聊天模式
- **聊天模式 (GEMINI)**: 與 Google Gemini AI 進行自然語言對話
- **電影查詢 (SEARCH_MOVIE)**: 搜尋 TMDB 電影資料庫，獲取詳細電影資訊
- **以圖搜片 (GUESS_MOVIE)**: 上傳電影劇照或海報，AI 自動識別電影
- **字幕翻譯 (SUB_TRANSLATE)**: 自動生成影片字幕並翻譯成多國語言

### 🛠 技術特點
- 支援 LINE Bot 和網頁版雙重介面
- 多媒體檔案處理 (圖片、音訊、影片)
- 即時字幕生成與嵌入
- 多語言翻譯支援
- 模組化架構設計

## 🏗 技術架構

### 主要技術棧
- **後端框架**: Flask
- **AI服務**: Google Gemini
- **聊天平台**: LINE Bot SDK
- **雲端服務**: Microsoft Azure (翻譯、語音、語言分析)
- **電影資料**: TMDB API
- **多媒體處理**: FFmpeg
- **前端**: HTML/CSS/JavaScript

### 專案結構
```
📦 1131_Chatbot_Final
├── 📄 app.py              # Flask 主應用程式
├── 📄 requirements.txt    # Python 依賴套件
├── 📄 config.ini         # 配置檔案 (需自行建立)
├── 📁 modules/           # 功能模組
│   ├── 📄 __init__.py
│   ├── 📄 config.py      # 配置管理
│   ├── 📄 line.py        # LINE Bot 處理
│   ├── 📄 gemini.py      # Gemini AI 整合
│   ├── 📄 tmdb.py        # 電影資料庫
│   ├── 📄 azure.py       # Azure 服務
│   ├── 📄 subtitle.py    # 字幕處理
│   └── 📄 translate_sub.py # 字幕翻譯
├── 📁 templates/         # HTML 模板
│   └── 📄 index.html
├── 📁 static/            # 靜態資源
│   ├── 📁 css/
│   ├── 📁 js/
│   └── 📁 images/
├── 📁 uploads/           # 上傳檔案存放
└── 📁 outputs/           # 輸出檔案存放
```

## 🚀 快速開始

### 1. 環境需求
- Python 3.8+
- FFmpeg (用於影片處理)

### 2. 安裝依賴
```bash
# 安裝 Python 套件
pip install -r requirements.txt

# 安裝 FFmpeg (依作業系統而定)
# Windows: 下載並安裝 FFmpeg
```

### 3. 設定 API 金鑰

由於 `config.ini` 包含敏感的 API 金鑰資訊，已加入 `.gitignore`，需要手動建立。

在專案根目錄建立 `config.ini` 檔案，內容如下：

```ini
[test]
message = Test World :wink:

[Line]
CHANNEL_ACCESS_TOKEN=你的_LINE_CHANNEL_ACCESS_TOKEN
CHANNEL_SECRET=你的_LINE_CHANNEL_SECRET

[Gemini]
API_KEY=你的_GOOGLE_GEMINI_API_KEY

[AzureTranslator]
Key=你的_AZURE_TRANSLATOR_KEY
Region=你的_AZURE_REGION
EndPoint=https://api.cognitive.microsofttranslator.com/

[AzureSpeech]
SPEECH_KEY=你的_AZURE_SPEECH_KEY
SPEECH_REGION=你的_AZURE_SPEECH_REGION

[TMDB]
API_KEY=你的_TMDB_API_KEY

[AzureLanguage]
API_KEY=你的_AZURE_LANGUAGE_API_KEY
END_POINT=你的_AZURE_LANGUAGE_ENDPOINT
```

### 4. 取得 API 金鑰

#### LINE Bot
1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 建立新的 Channel (Messaging API)
3. 取得 Channel Access Token 和 Channel Secret

#### Google Gemini
1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 建立 API 金鑰

#### Microsoft Azure
1. 註冊 [Azure 帳號](https://azure.microsoft.com/)
2. 建立翻譯器、語音服務和語言理解資源
3. 取得對應的金鑰和端點

#### TMDB
1. 註冊 [TMDB 帳號](https://www.themoviedb.org/)
2. 申請 API 金鑰

### 5. 執行應用程式
```bash
python app.py
```

網頁版將在 `http://localhost:5000` 開啟

## 📱 使用指南

### 網頁版使用
1. 開啟瀏覽器，前往 `http://localhost:5000`
2. 選擇聊天模式：
   - **聊天**: 與 AI 自由對話
   - **查詢資料庫**: 搜尋電影資訊
   - **以圖搜尋**: 上傳圖片識別電影
   - **字幕翻譯**: 上傳影片生成翻譯字幕
3. 輸入訊息或上傳檔案
4. 查看 AI 回應

### LINE Bot 使用
1. 將 Bot 加為好友
2. 發送文字、圖片或語音訊息
3. Bot 會根據當前模式回應

### 字幕翻譯功能
1. 切換到「字幕翻譯」模式
2. 上傳影片檔案 (支援 mp4, avi, mov 等格式)
3. 指定目標語言 (如: zh-TW, en, ja, ko)
4. 系統自動生成字幕並翻譯
5. 下載包含字幕的影片檔案

## 🔄 專案管理

### 待辦事項
專案待辦清單：https://github.com/orgs/yzu-1131-cs322-chatbot-g1/projects/7

請於認領任務前：
1. 設定 Assignee (指派給自己)
2. 更新任務狀態

### 開發指南

#### 模組開發
將獨立功能封裝成模組，放置於 `modules/` 資料夾：

```python
# 匯入整個模組
from modules import ModuleName

# 匯入特定類別或函式
from modules.ModuleName import ClassName, FunctionName

# 範例：匯入設定管理
from modules.config import config
```

#### Git 版本管理
- **提交頻率**: 每個 commit 應該是一個完整、獨立的功能
- **推送前檢查**: 
  ```bash
  git pull          # 取得最新變更
  git status        # 檢查檔案狀態
  git add .         # 加入變更
  git commit -m "描述變更內容"
  git push          # 推送變更
  ```
- **衝突處理**: 發生合併衝突時，請先解決衝突再推送

## 🤝 貢獻指南

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 授權條款

此專案為 YZU CS322 課程作業專案。

## 🆘 常見問題

### Q: 執行時出現 "No module named 'xxx'" 錯誤
A: 請確認已安裝所有依賴套件：`pip install -r requirements.txt`

### Q: 字幕翻譯功能無法使用
A: 請檢查：
1. FFmpeg 是否正確安裝
2. Azure 翻譯服務 API 金鑰是否正確設定
3. 影片格式是否支援

### Q: LINE Bot 無法回應
A: 請檢查：
1. LINE Channel 設定是否正確
2. Webhook URL 是否設定正確
3. API 金鑰是否有效

### Q: Gemini AI 無法回應
A: 請確認 Google Gemini API 金鑰是否正確設定且有效

---

💡 **提示**: 如有任何問題或建議，歡迎開啟 Issue 或聯繫開發團隊！
