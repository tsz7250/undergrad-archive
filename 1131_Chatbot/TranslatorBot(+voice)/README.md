# 語音翻譯聊天機器人 (TranslatorBot+voice)

進階版翻譯機器人，整合 Azure Translation 和 Speech Services，支援語音輸入和語音輸出功能，提供完整的語音翻譯體驗。

## 🚀 功能特色

- **語音輸入**: 支援語音訊息的語音識別
- **文字翻譯**: 使用 Azure Translation Service 進行翻譯
- **語音輸出**: 將翻譯結果轉換為語音檔案
- **多語言語音**: 支援多種語言的語音合成
- **Line Bot 整合**: 透過 Line 平台提供完整的語音翻譯服務
- **音檔處理**: 使用 librosa 進行音訊優化

## 🛠️ 使用技術

- **Azure Translation Service**: 多語言文字翻譯
- **Azure Speech Service**: 語音識別和語音合成
- **Line Messaging API**: Line Bot 平台整合
- **Python Flask**: Web 應用程式框架
- **librosa**: 音訊處理和分析
- **ConfigParser**: 配置檔案管理

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
```

2. 設定步驟：
   - 建立 Line Developer 帳號和 Messaging API Channel
   - 建立 Azure 認知服務訂閱
   - 建立 Translation Service 和 Speech Service 資源
   - 取得相關 API 金鑰和端點
   - 設定 Line Bot webhook URL

## 🚀 執行應用程式

```bash
python app.py
```

應用程式將啟動 Flask 伺服器，並開始監聽 Line webhook 事件。

## 💬 使用方式

### 文字翻譯
1. 傳送文字訊息給 Bot
2. 接收翻譯結果和語音檔案

### 語音翻譯
1. 傳送語音訊息給 Bot
2. Bot 會識別語音內容
3. 翻譯識別的文字
4. 回傳翻譯結果和目標語言語音

## 🗣️ 語音功能

### 語音識別 (Speech-to-Text)
- **多語言識別**: 支援多種語言的語音識別
- **高準確率**: 使用 Azure Speech Service 企業級識別
- **噪音處理**: 智能過濾背景噪音
- **實時處理**: 快速處理語音輸入

### 語音合成 (Text-to-Speech)
- **自然語音**: 高品質的人工語音合成
- **多語言語音**: 支援各種語言的本地語音
- **語音選擇**: 可選擇不同的語音角色
- **音質優化**: 使用 librosa 優化音檔品質

## 🌍 語言支援

支援 Azure 服務的所有語言，包括：
- **語音識別語言**: 70+ 種語言
- **翻譯語言**: 100+ 種語言  
- **語音合成語言**: 75+ 種語言

常用語言組合：
- 中文 ↔ 英文
- 中文 ↔ 日文
- 英文 ↔ 日文
- 等等...

## 🔧 音訊處理

使用 librosa 進行：
- **音檔格式轉換**: 確保與 Line 平台相容
- **音質優化**: 提升語音清晰度
- **音量正規化**: 統一音量大小
- **噪音減少**: 過濾背景雜音

## 📁 檔案結構

```
TranslatorBot(+voice)/
├── app.py              # 主要應用程式
├── config.ini          # 配置檔案 (需自行建立)
├── requirements.txt    # Python 相依套件
└── static/            # 靜態檔案目錄 (音檔存放)
```

## 🎵 音檔管理

- **暫存機制**: 臨時存放處理中的音檔
- **格式支援**: 支援多種音檔格式
- **大小限制**: 符合 Line 平台的檔案大小限制
- **自動清理**: 定期清理暫存音檔

## 🚀 進階功能

### 語音設定自訂
```python
# 語音識別設定
speech_recognizer_config.speech_recognition_language = "zh-TW"

# 語音合成設定  
speech_synthesizer_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"
```

### 翻譯選項
- 來源語言自動偵測
- 目標語言設定
- 專業術語處理
- 語境理解優化

## 📊 效能最佳化

- **並行處理**: 同時處理語音和翻譯
- **快取機制**: 避免重複處理相同內容
- **錯誤重試**: 自動重試失敗的請求
- **資源管理**: 有效管理記憶體和儲存空間

## 📝 注意事項

- 需要 Azure 認知服務完整訂閱
- 語音處理需要較多運算資源
- Azure 服務會產生較高費用
- 音檔大小需符合 Line 限制 (最大 10MB)
- 建議監控 API 使用量
- 確保網路連線穩定以處理音檔

## 💰 成本考量

Azure 服務計費：
- **Speech-to-Text**: 按分鐘計費
- **Text-to-Speech**: 按字符數計費
- **Translation**: 按字符數計費

建議設定使用量警告以控制成本。