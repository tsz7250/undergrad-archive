# 文字轉語音聊天機器人 (TextToSpeech)

整合 Azure Translation 和 Speech Services 的 Line Bot，提供文字翻譯和語音合成功能，讓使用者能夠聽到翻譯後的語音。

## 🚀 功能特色

- **多語言翻譯**: 使用 Azure Translation Service 進行文字翻譯
- **語音合成**: 使用 Azure Speech Service 將文字轉換為語音
- **Line Bot 整合**: 透過 Line 平台提供服務
- **音檔處理**: 使用 librosa 進行音訊檔案處理
- **多語音支援**: 支援多種語言的語音輸出

## 🛠️ 使用技術

- **Azure Translation Service**: 多語言文字翻譯
- **Azure Speech Service**: 語音合成和語音識別
- **Line Messaging API**: Line Bot 平台整合
- **Python Flask**: Web 應用程式框架
- **librosa**: 音訊處理函式庫
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

1. 將 Line Bot 加入好友
2. 傳送要翻譯的文字訊息
3. Bot 會回傳翻譯結果和語音檔案
4. 點擊播放按鈕聽取語音

### 指令格式
- 直接輸入文字：預設翻譯功能
- 特定指令：可能支援語言選擇 (詳見程式碼)

## 🗣️ 語音功能

- **語音合成**: 將翻譯後的文字轉換為語音
- **音檔格式**: 支援 Line 平台的音訊格式
- **語音品質**: 使用 Azure Speech Service 高品質語音
- **多語言語音**: 支援多種語言的本地語音

## 🌍 翻譯功能

- **多語言支援**: 支援 Azure Translation Service 的所有語言
- **自動偵測**: 可自動偵測來源語言
- **準確翻譯**: 使用 Azure 企業級翻譯服務
- **即時處理**: 快速回應翻譯請求

## 🔧 進階設定

### Azure Speech 設定
```python
speech_config = speechsdk.SpeechConfig(
    subscription=config['AzureSpeech']['SPEECH_KEY'], 
    region=config['AzureSpeech']['SPEECH_REGION']
)
speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"  # 可調整語音
```

### 音檔處理
使用 librosa 進行音訊檔案的處理和優化，確保在 Line 平台上的播放品質。

## 📁 檔案結構

```
TextToSpeech/
├── app.py              # 主要應用程式
├── config.ini          # 配置檔案 (需自行建立)
├── requirements.txt    # Python 相依套件
└── static/            # 靜態檔案目錄 (音檔存放)
```

## 🎵 音檔管理

- 生成的語音檔案存放在 `static/` 目錄
- 支援多種音檔格式
- 自動清理機制避免磁碟空間不足
- 確保音檔符合 Line 平台規範

## 📝 注意事項

- 需要有效的 Azure 認知服務訂閱
- 需要 Line Developer 帳號和 Channel
- Azure 服務使用會產生費用
- 確保 webhook URL 使用 HTTPS
- 音檔大小需符合 Line 平台限制
- 建議監控 API 使用量以控制成本