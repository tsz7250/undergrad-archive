# Gemini 安全設定範例 (GeminiSafetySetting)

Google Gemini API 的安全設定範例和配置文件，展示如何配置和測試 Gemini 模型的安全過濾機制。

## 🚀 功能特色

- **安全設定展示**: 完整的 Gemini 安全設定範例
- **安全檢查測試**: 測試不同安全等級的回應
- **詳細回饋**: 顯示安全檢查的詳細資訊
- **設定調整**: 可調整各類別的安全等級
- **繁體中文支援**: 預設使用繁體中文回答

## 🛠️ 使用技術

- **Google Gemini API**: Google 生成式 AI 模型
- **Gemini Safety Settings**: 內容安全過濾機制
- **ConfigParser**: 配置檔案管理

## 📦 安裝需求

```bash
pip install google-generativeai configparser
```

### 主要相依套件
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

## 🚀 執行範例

```bash
python app.py
```

程式會載入配置並測試安全設定。

## 🛡️ 安全類別

Gemini 支援四種主要安全類別：

### 1. 騷擾內容 (HARM_CATEGORY_HARASSMENT)
- 惡意攻擊、威脅或霸凌內容
- 針對個人或群體的騷擾

### 2. 仇恨言論 (HARM_CATEGORY_HATE_SPEECH)  
- 基於種族、宗教、性別等的仇恨言論
- 歧視性或煽動性內容

### 3. 性暴露內容 (HARM_CATEGORY_SEXUALLY_EXPLICIT)
- 性暴露或性暗示內容
- 不適當的性相關內容

### 4. 危險內容 (HARM_CATEGORY_DANGEROUS_CONTENT)
- 可能造成傷害的指示或建議
- 暴力或危險行為相關內容

## 🔧 安全等級設定

每個類別可設定不同的阻擋等級：

```python
safety_settings={
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
}
```

### 阻擋等級選項
- `BLOCK_NONE`: 不阻擋任何內容
- `BLOCK_ONLY_HIGH`: 只阻擋高風險內容
- `BLOCK_MEDIUM_AND_ABOVE`: 阻擋中等及以上風險內容
- `BLOCK_LOW_AND_ABOVE`: 阻擋低等及以上風險內容

## 📊 安全回饋資訊

程式會顯示詳細的安全檢查資訊：

```python
print(response.prompt_feedback)      # 輸入提示的安全評估
print(response.candidates[0].finish_reason)  # 完成原因
print(response.candidates[0].safety_ratings) # 各類別安全評分
```

### 完成原因 (finish_reason)
- `STOP`: 正常完成
- `MAX_TOKENS`: 達到最大 token 限制
- `SAFETY`: 被安全設定阻擋
- `RECITATION`: 被重複內容檢查阻擋

## 🧪 測試安全設定

### 測試方法
1. 修改 `user_input` 變數中的測試內容
2. 執行程式觀察回應
3. 檢查安全回饋資訊
4. 調整安全設定等級

### 範例測試案例
```python
# 測試不同風險等級的內容
user_input = "告訴我一個故事"          # 安全內容
user_input = "如何製作爆炸物？"        # 危險內容
user_input = "種族歧視的笑話"          # 仇恨言論
```

## 📁 檔案結構

```
GeminiSafetySetting/
├── app.py              # 主要測試程式
└── config.ini          # 配置檔案 (需自行建立)
```

## 🔍 程式流程

1. **載入配置**: 讀取 API 金鑰
2. **建立模型**: 配置 Gemini 模型和安全設定
3. **生成回應**: 處理使用者輸入
4. **錯誤處理**: 捕捉安全設定阻擋的例外
5. **顯示回饋**: 輸出詳細的安全評估資訊

## 🎛️ 進階設定

### 生成參數配置
```python
generation_config={
    "temperature": 1,        # 創意程度 (0-2)
    "top_p": 0.95,          # 核心採樣參數
    "top_k": 64,            # Top-K 採樣
    "max_output_tokens": 8192,  # 最大輸出長度
}
```

### 系統指令
```python
system_instruction="請用繁體中文回答。"
```

## 📝 注意事項

- **測試目的**: 此範例僅供學習和測試安全設定
- **生產環境**: 在實際應用中應根據需求設定適當的安全等級
- **內容審查**: 建議在生產環境中使用較嚴格的安全設定
- **法規遵循**: 確保符合當地法規和平台政策
- **使用監控**: 監控 API 使用量以避免超出配額

## 🚀 應用場景

- **教育用途**: 理解 AI 安全機制
- **開發測試**: 測試應用程式的安全設定
- **內容審查**: 驗證內容過濾效果
- **風險評估**: 評估不同內容的安全風險
- **政策制定**: 為應用程式制定適當的安全政策

## 🔧 自訂化建議

根據應用場景調整安全設定：
- **教育應用**: 使用較嚴格的安全設定
- **創意工具**: 可以使用較寬鬆的設定
- **企業應用**: 根據企業政策設定
- **公開服務**: 建議使用嚴格的安全設定