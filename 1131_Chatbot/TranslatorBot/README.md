# 翻譯聊天機器人 (TranslatorBot)

使用 Azure Translation Service 的 Line Bot，提供即時多語言翻譯服務，讓使用者能夠輕鬆進行跨語言溝通。

## 🚀 功能特色

- **即時翻譯**: 使用 Azure Translation Service 進行高品質翻譯
- **多語言支援**: 支援 Azure Translation 的所有語言對
- **Line Bot 整合**: 透過 Line 平台提供便利的翻譯服務
- **自動語言偵測**: 可自動偵測來源語言
- **快速回應**: 即時處理並回傳翻譯結果

## 🛠️ 使用技術

- **Azure Translation Service**: Microsoft 企業級翻譯服務
- **Line Messaging API**: Line Bot 平台整合
- **Python Flask**: Web 應用程式框架
- **ConfigParser**: 配置檔案管理

## 📦 安裝需求

```bash
pip install -r requirements.txt
```

### 相依套件
- line-bot-sdk
- flask
- configparser
- azure-ai-translation-text==1.0.0

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
```

2. 設定步驟：
   - 建立 Line Developer 帳號和 Messaging API Channel
   - 建立 Azure 認知服務訂閱
   - 建立 Translation Service 資源
   - 取得 API 金鑰、端點和區域資訊
   - 設定 Line Bot webhook URL 指向你的應用程式

## 🚀 執行應用程式

```bash
python app.py
```

應用程式將啟動 Flask 伺服器，並開始監聽 Line webhook 事件。

## 💬 使用方式

1. 將 Line Bot 加入好友
2. 傳送要翻譯的文字訊息
3. Bot 會自動偵測語言並翻譯成目標語言
4. 即時收到翻譯結果

### 基本指令
- 直接輸入文字：自動翻譯
- 可能支援語言指定格式 (詳見程式碼實作)

## 🌍 支援語言

Azure Translation Service 支援超過 100 種語言，包括：

**常用語言**：
- 繁體中文 (zh-Hant)
- 簡體中文 (zh-Hans)
- 英文 (en)
- 日文 (ja)
- 韓文 (ko)
- 法文 (fr)
- 德文 (de)
- 西班牙文 (es)
- 等等...

## 🔧 翻譯功能

- **高品質翻譯**: 使用 Microsoft 企業級翻譯引擎
- **語言自動偵測**: 智能識別來源語言
- **上下文理解**: 考慮語境進行準確翻譯
- **即時處理**: 快速回應翻譯請求
- **錯誤處理**: 完善的錯誤處理機制

## 🔧 進階設定

### 自訂翻譯選項
可以在程式中設定：
- 目標語言偏好
- 翻譯品質等級
- 專業術語翻譯
- 翻譯結果格式化

### API 最佳化
- 批次處理請求
- 快取機制
- 錯誤重試邏輯
- 使用量監控

## 📁 檔案結構

```
TranslatorBot/
├── app.py              # 主要應用程式
├── config.ini          # 配置檔案 (需自行建立)
└── requirements.txt    # Python 相依套件
```

## 🛡️ 安全性考量

- API 金鑰安全存儲
- HTTPS 通訊協定
- 輸入內容驗證
- 錯誤訊息不洩漏敏感資訊

## 📊 使用監控

建議監控項目：
- API 呼叫次數
- 翻譯字符數量
- 回應時間
- 錯誤率統計

## 💰 成本控制

Azure Translation Service 按使用量收費：
- 監控每月翻譯字符數
- 設定使用量警告
- 優化請求效率
- 避免重複翻譯相同內容

## 📝 注意事項

- 需要有效的 Azure 認知服務訂閱
- 需要 Line Developer 帳號和 Channel
- Azure Translation Service 會產生使用費用
- 確保 webhook URL 使用 HTTPS 協定
- 建議設定 API 使用量警告
- 注意翻譯內容的隱私保護