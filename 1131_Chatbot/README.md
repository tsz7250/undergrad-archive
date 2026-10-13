# 1131 - 微型應用程式設計實務 作業集合

此為 1131 學期「微型應用程式設計實務」課程的作業和專案程式碼集合。

## 📋 專案概覽

本倉庫包含多個 AI 聊天機器人和微型應用程式專案，主要使用 Python 開發，整合了多種 AI 服務和技術。

## 🤖 專案列表

### 1. [LLM_Chatbot](./LLM_Chatbot/) - Gemini 網頁聊天機器人
使用 Google Gemini API 建立的網頁版聊天機器人，具備安全設定和對話功能。

### 2. [LLM_Line](./LLM_Line/) - Gemini Line 聊天機器人  
整合 Google Gemini API 的 Line Bot，提供智能對話服務。

### 3. [LangChain](./LangChain/) - LangChain 應用程式
基於 LangChain 框架開發的 AI 應用程式。

### 4. [SentimentAnalysis](./SentimentAnalysis/) - 情感分析機器人
Line 聊天機器人，使用 Microsoft Language Service 進行情感分析，判斷文字的正向、負向或中性情緒。

### 5. [TextToSpeech](./TextToSpeech/) - 文字轉語音機器人
整合 Azure Translation 和 Speech Services 的 Line Bot，提供文字翻譯和語音合成功能。

### 6. [TranslatorBot](./TranslatorBot/) - 翻譯機器人
使用 Azure Translation Service 的 Line Bot，提供多語言翻譯服務。

### 7. [TranslatorBot(+voice)](./TranslatorBot(+voice)/) - 語音翻譯機器人
進階版翻譯機器人，支援語音輸入和語音輸出功能。

### 8. [TranslatorWeb](./TranslatorWeb/) - 網頁翻譯應用
基於 Flask 的網頁翻譯應用程式，整合 Azure 翻譯和語音服務。

### 9. [GeminiSafetySetting](./GeminiSafetySetting/) - Gemini 安全設定
Google Gemini API 的安全設定範例和配置文件。

## 🛠️ 技術棧

- **程式語言**: Python
- **Web 框架**: Flask
- **AI 服務**: 
  - Google Gemini API
  - Microsoft Azure Cognitive Services
  - LangChain
- **聊天平台**: Line Messaging API
- **其他服務**: Azure Translation, Azure Speech Services

## 📦 安裝需求

每個專案都有自己的 `requirements.txt` 文件，請參閱各專案的 README 了解詳細安裝說明。

## ⚙️ 配置文件

多數專案需要 `config.ini` 配置文件來設定 API 金鑰和服務端點。請參考各專案的說明文件進行配置。

## 🚀 快速開始

1. 選擇想要執行的專案
2. 進入該專案目錄
3. 安裝相依套件：`pip install -r requirements.txt`
4. 配置 `config.ini` 文件
5. 執行應用程式：`python app.py`

## 📄 授權

此專案僅供學習和教育用途。