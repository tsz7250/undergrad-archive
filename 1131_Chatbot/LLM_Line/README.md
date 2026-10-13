# Gemini Line 聊天機器人 (LLM_Line)

整合 Google Gemini API 的 Line Bot，透過 Line 平台提供智能對話服務，具備完整的安全設定和角色扮演功能。

## 🚀 功能特色

- **Gemini AI 整合**: 使用 Google Gemini 1.5 Flash 模型
- **Line Bot 平台**: 透過 Line Messaging API 提供服務
- **角色扮演**: 可自訂 AI 角色和對話風格
- **圖片上傳支援**: 支援靜態檔案處理
- **安全設定**: 完整的 Gemini 安全設定配置
- **繁體中文支援**: 優化繁體中文對話體驗

## 🛠️ 使用技術

- **Google Gemini API**: 生成式 AI 對話模型
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
- google-generativeai

## ⚙️ 配置設定

1. 建立 `config.ini` 配置檔案：

```ini
[Line]
CHANNEL_ACCESS_TOKEN = 你的_Line_Channel_Access_Token
CHANNEL_SECRET = 你的_Line_Channel_Secret

[Gemini]
API_KEY = 你的_Google_Gemini_API_金鑰
```

2. 設定步驟：
   - 建立 Line Developer 帳號和 Messaging API Channel
   - 取得 Google Gemini API 金鑰
   - 設定 Line Bot webhook URL 指向你的應用程式
   - 將 API 金鑰和 tokens 填入配置檔案

## 🚀 執行應用程式

```bash
python app.py
```

應用程式將啟動 Flask 伺服器，並開始監聽 Line webhook 事件。

## 💬 使用方式

1. 將 Line Bot 加入好友
2. 傳送文字訊息給機器人
3. AI 會根據預設角色回應
4. 支援連續對話和上下文理解

## 🎭 AI 角色設定

在 `app.py` 中可以找到 `llm_role_description` 變數來自訂 AI 的角色：
- 個性特徵
- 回答風格
- 專業領域
- 對話目標

## 🛡️ 安全設定

應用程式配置了完整的 Gemini 安全設定：
- 騷擾內容過濾
- 仇恨言論檢測
- 性暴露內容篩選
- 危險內容防護

當前設定為較寬鬆模式，可根據需求調整。

## 🔧 進階設定

### AI 模型參數調整
```python
generation_config={
    "temperature": 1,        # 創意程度 (0-2)
    "top_p": 0.95,          # 核心採樣 (0-1)
    "top_k": 64,            # Top-K 採樣
    "max_output_tokens": 8192,  # 最大回應長度
}
```

### Webhook 設定
確保你的應用程式部署在可從外部存取的伺服器上，並在 Line Developer Console 中設定正確的 webhook URL。

## 📁 檔案結構

```
LLM_Line/
├── app.py              # 主要應用程式
├── config.ini          # 配置檔案 (需自行建立)
├── requirements.txt    # Python 相依套件
└── static/            # 靜態檔案目錄
```

## 📝 注意事項

- 需要有效的 Line Developer 帳號和 Channel
- 需要 Google Gemini API 金鑰和相關權限
- 確保 webhook URL 使用 HTTPS 協定
- API 使用可能產生費用，請注意用量
- 測試時建議先在開發環境中驗證功能