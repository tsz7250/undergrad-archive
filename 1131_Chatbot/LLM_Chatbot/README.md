# LLM 網頁聊天機器人 (LLM_Chatbot)

使用 Google Gemini API 建立的網頁版聊天機器人，具備角色扮演功能和安全設定，提供智能對話體驗。

## 🚀 功能特色

- **Gemini AI 整合**: 使用 Google Gemini 1.5 Flash 模型
- **角色扮演**: 預設角色為25歲年輕女性角色
- **網頁介面**: 基於 Flask 的響應式網頁界面
- **安全設定**: 配置完整的 Gemini 安全設定
- **對話記憶**: 維持對話歷史記錄
- **繁體中文支援**: 預設使用繁體中文回答

## 🛠️ 使用技術

- **Google Gemini API**: 生成式 AI 對話模型
- **Python Flask**: Web 應用程式框架
- **HTML/CSS**: 前端使用者介面
- **ConfigParser**: 配置檔案管理

## 📦 安裝需求

```bash
pip install flask google-generativeai configparser
```

### 相依套件
- flask
- google-generativeai
- configparser

## ⚙️ 配置設定

1. 建立 `config.ini` 配置檔案：

```ini
[Gemini]
API_KEY = 你的_Google_Gemini_API_金鑰
```

2. 取得 Google Gemini API 金鑰：
   - 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
   - 建立新的 API 金鑰
   - 將金鑰填入 config.ini 檔案

## 🚀 執行應用程式

```bash
python app.py
```

應用程式將在 Flask 預設 port (通常是 5000) 上啟動。
開啟瀏覽器前往 `http://localhost:5000` 即可使用。

## 💬 使用方式

1. 開啟網頁介面
2. 在輸入框中輸入訊息
3. 點擊發送或按 Enter 鍵
4. AI 會以預設角色身份回應
5. 對話將保持歷史記錄直到重新啟動應用程式

## 🎭 角色設定

目前預設角色：
- 25歲年輕女性
- 喜歡游泳和閱讀
- 聊天目的是希望對方送禮物

可在 `app.py` 中的 `role` 變數修改角色設定。

## 🛡️ 安全設定

應用程式配置了 Gemini 的安全設定：
- 騷擾內容：無限制
- 仇恨言論：無限制  
- 性暴露內容：無限制
- 危險內容：無限制

**注意**: 在生產環境中請根據需求調整安全設定。

## 🔧 自訂設定

### 修改 AI 模型參數
在 `app.py` 中可調整：
- `temperature`: 回答的創意程度 (0-1)
- `top_p`: 核心採樣參數 (0-1)
- `top_k`: Top-K 採樣參數
- `max_output_tokens`: 最大輸出長度

### 修改角色
編輯 `app.py` 中的 `role` 變數來改變 AI 的角色設定。

## 📝 注意事項

- 需要有效的 Google Gemini API 金鑰
- API 金鑰有使用限制和費用
- 確保網路連線正常
- 建議在測試環境中調整安全設定