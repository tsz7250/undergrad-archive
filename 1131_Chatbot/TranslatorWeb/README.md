# 網頁翻譯應用程式 (TranslatorWeb)

基於 Flask 的網頁翻譯應用程式，整合 Azure 翻譯、語音和文字分析服務，提供完整的多模態翻譯體驗。

## 🚀 功能特色

- **網頁介面**: 友善的 Web UI 翻譯界面
- **多服務整合**: 整合 Azure Translation、Speech 和 Text Analytics
- **文字翻譯**: 高品質的多語言翻譯
- **語音合成**: 將翻譯結果轉換為語音
- **文字分析**: 提供情感分析和關鍵詞擷取
- **響應式設計**: 支援各種裝置的瀏覽器存取
- **Line Bot 支援**: 同時支援 Line Bot 功能

## 🛠️ 使用技術

- **Azure Translation Service**: 多語言翻譯
- **Azure Speech Service**: 語音合成和識別  
- **Azure Text Analytics**: 文字分析和情感分析
- **Python Flask**: Web 應用程式框架
- **HTML/CSS/JavaScript**: 前端使用者介面
- **librosa**: 音訊處理
- **Line Messaging API**: Line Bot 整合

## 📦 安裝需求

```bash
pip install -r requirements.txt
```

### 相依套件
- line-bot-sdk
- flask
- configparser
- azure-ai-translation-text
- azure-cognitiveservices-speech
- azure-ai-textanalytics
- librosa

## ⚙️ 配置設定

1. 建立 `config.ini` 配置檔案：

```ini
[Line]
CHANNEL_ACCESS_TOKEN = 你的_Line_Channel_Access_Token
CHANNEL_SECRET = 你的_Line_Channel_Secret

[AzureTranslation]
TRANSLATION_KEY = 你的_Azure_Translation_金鑰
TRANSLATION_ENDPOINT = 你的_Azure_Translation_端點
TRANSLATION_REGION = 你的_Azure_Translation_區域

[AzureSpeech]
SPEECH_KEY = 你的_Azure_Speech_金鑰
SPEECH_REGION = 你的_Azure_Speech_區域

[AzureTextAnalytics]
TEXT_ANALYTICS_KEY = 你的_Azure_Text_Analytics_金鑰
TEXT_ANALYTICS_ENDPOINT = 你的_Azure_Text_Analytics_端點
```

2. 建立所需的 Azure 服務資源：
   - Azure Translation Service
   - Azure Speech Service  
   - Azure Text Analytics Service
   - Line Developer Channel (可選)

## 🚀 執行應用程式

```bash
python app.py
```

應用程式將在 Flask 預設 port 上啟動，通常是 `http://localhost:5000`

## 💻 網頁功能

### 主要功能
1. **文字翻譯**
   - 輸入來源文字
   - 選擇來源和目標語言
   - 即時翻譯結果顯示

2. **語音功能**
   - 播放翻譯結果的語音
   - 下載語音檔案
   - 調整語音設定

3. **文字分析**
   - 情感分析結果
   - 關鍵詞擷取
   - 語言偵測

## 🌐 網頁介面特色

- **直觀設計**: 清晰簡潔的使用者界面
- **即時回饋**: 即時顯示翻譯和分析結果
- **多語言支援**: 支援 100+ 種語言翻譯
- **響應式布局**: 適應不同螢幕大小
- **音檔播放**: 內建音訊播放器

## 📁 檔案結構

```
TranslatorWeb/
├── app.py              # 主要應用程式
├── config.ini          # 配置檔案 (需自行建立)
├── requirements.txt    # Python 相依套件
├── static/             # 靜態檔案 (CSS, JS, 音檔)
│   ├── css/           # 樣式檔案
│   ├── js/            # JavaScript 檔案
│   └── audio/         # 生成的音檔
└── templates/          # HTML 模板
    └── index.html     # 主頁面模板
```

## 🎨 前端功能

### HTML 模板 (`templates/index.html`)
- 翻譯輸入表單
- 結果顯示區域
- 語音播放控制
- 語言選擇下拉選單

### 靜態資源 (`static/`)
- CSS 樣式檔案
- JavaScript 互動邏輯
- 生成的音檔存放

## 🔧 API 端點

- `GET /`: 主頁面
- `POST /translate`: 翻譯 API
- `POST /analyze`: 文字分析 API  
- `POST /synthesize`: 語音合成 API
- `POST /callback`: Line Bot webhook (可選)

## 🌍 支援語言

支援 Azure 服務的所有語言：
- **翻譯**: 100+ 種語言
- **語音合成**: 75+ 種語言
- **文字分析**: 50+ 種語言

## 📊 文字分析功能

- **情感分析**: 正向/負向/中性情感偵測
- **關鍵詞擷取**: 自動提取重要詞彙
- **語言偵測**: 自動識別文字語言
- **實體識別**: 識別人名、地名等實體

## 🎵 音檔處理

- **格式支援**: MP3, WAV 等常見格式
- **品質優化**: 使用 librosa 優化音質
- **快取機制**: 避免重複生成相同音檔
- **自動清理**: 定期清理暫存音檔

## 🛡️ 安全性設定

- **API 金鑰保護**: 安全存儲在配置檔案
- **輸入驗證**: 防止惡意輸入
- **CORS 設定**: 適當的跨域請求設定
- **錯誤處理**: 不洩漏敏感資訊

## 📱 跨平台支援

- **桌面瀏覽器**: Chrome, Firefox, Safari, Edge
- **行動瀏覽器**: 支援手機和平板瀏覽器
- **PWA 友善**: 可安裝為網頁應用程式

## 📝 注意事項

- 需要完整的 Azure 認知服務訂閱
- 多項服務會產生累積費用
- 確保網路連線穩定
- 建議監控各項服務的使用量
- 大量使用時注意 API 配額限制