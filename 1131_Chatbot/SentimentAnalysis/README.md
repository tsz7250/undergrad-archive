# 情感分析聊天機器人 (SentimentAnalysis)

製作 Line 聊天機器人，能夠判斷使用者輸入文字的情感傾向，分析結果包含正向、負向或中性情緒。

## 🚀 功能特色

- **情感分析**: 自動分析文字的情感傾向
- **Line Bot 整合**: 透過 Line Messaging API 提供服務
- **即時回饋**: 即時回傳分析結果
- **多語言支援**: 支援繁體中文情感分析

## 🛠️ 使用技術

- **Line Messaging API**: Line Bot 平台整合
- **Python Flask**: Web 應用程式框架
- **Microsoft Language Service**: Azure 認知服務進行情感分析
- **ConfigParser**: 配置檔案管理

## 📦 安裝需求

```bash
pip install -r requirements.txt
```

### 相依套件
- line-bot-sdk
- flask
- configparser

## ⚙️ 配置設定

1. 建立 `config.ini` 配置檔案：

```ini
[Line]
CHANNEL_ACCESS_TOKEN = 你的_Line_Channel_Access_Token
CHANNEL_SECRET = 你的_Line_Channel_Secret

[Azure]
LANGUAGE_KEY = 你的_Azure_Language_Service_金鑰
LANGUAGE_ENDPOINT = 你的_Azure_Language_Service_端點
```

2. 設定 Line Bot webhook URL 指向你的應用程式

## 🚀 執行應用程式

```bash
python app.py
```

應用程式將在預設 port 上啟動，並開始監聽 Line webhook 事件。

## 💬 使用方式

1. 將 Line Bot 加入好友
2. 傳送任何文字訊息給機器人
3. 機器人會回傳該文字的情感分析結果：
   - 😊 正向情緒
   - 😞 負向情緒  
   - 😐 中性情緒

## 🔧 開發說明

應用程式主要功能：
- 接收 Line webhook 訊息事件
- 將文字傳送至 Azure Language Service 進行分析
- 解析情感分析結果
- 回傳格式化的分析結果給使用者

## 📝 注意事項

- 需要有效的 Line Developer 帳號和 Channel
- 需要 Azure 認知服務訂閱和 Language Service 資源
- 確保 webhook URL 可從外部存取
- 建議使用 HTTPS 協定