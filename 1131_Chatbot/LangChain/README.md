# LangChain 圖像分析應用 (LangChain)

使用 LangChain 框架整合 Google Gemini API 的圖像分析應用程式，能夠分析圖片並以繁體中文回答相關問題。

## 🚀 功能特色

- **圖像理解**: 使用 Gemini 1.5 Flash 分析圖片內容
- **LangChain 整合**: 基於 LangChain 框架開發
- **多模態輸入**: 支援文字問題搭配圖片分析
- **繁體中文回答**: 自動以繁體中文回應
- **IPython 顯示**: 支援 Jupyter Notebook 環境

## 🛠️ 使用技術

- **LangChain**: AI 應用程式開發框架
- **Google Gemini API**: 多模態 AI 模型
- **langchain_google_genai**: Gemini 整合套件
- **IPython**: 互動式 Python 環境
- **ConfigParser**: 配置檔案管理

## 📦 安裝需求

安裝相依套件：
```bash
pip install langchain-google-genai langchain-core ipython configparser
```

### 主要相依套件
- langchain-core
- langchain-google-genai  
- ipython
- configparser

## ⚙️ 配置設定

1. 建立 `config.ini` 配置檔案：

```ini
[Gemini]
API_KEY = 你的_Google_Gemini_API_金鑰
```

2. 準備圖片檔案：
   - 將要分析的圖片放在專案目錄中
   - 目前範例使用 `animal.png`
   - 支援常見圖片格式 (PNG, JPG, JPEG)

## 🚀 執行應用程式

```bash
python app.py
```

或在 Jupyter Notebook 中執行相關程式碼區塊。

## 💬 使用方式

1. 修改 `user_input` 變數設定你想問的問題
2. 修改 `image_url` 指向你要分析的圖片
3. 執行程式，AI 會分析圖片並回答問題
4. 程式會同時顯示問題、答案和圖片

### 範例使用
```python
user_input = "在吃甚麼？"  # 你的問題
image_url = "animal.png"   # 圖片檔案路徑
```

## 🖼️ 圖片來源支援

- **本地檔案**: 相對路徑 (如 `animal.png`)
- **網路圖片**: HTTP/HTTPS URL
- **範例檔案**: 目前包含動物圖片範例

## 🔧 自訂設定

### 修改模型設定
```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",  # 可選其他 Gemini 模型
    google_api_key=config["Gemini"]["API_KEY"],
    temperature=0.7,  # 可調整創意程度
)
```

### 修改問題和圖片
在 `app.py` 中修改：
- `user_input`: 要問的問題
- `image_url`: 圖片檔案路徑或 URL

## 📁 檔案結構

```
LangChain/
├── app.py                              # 主要應用程式
├── app2.py                            # 替代版本
├── config.ini                         # 配置檔案 (需自行建立)
├── animal.png                         # 範例圖片
├── image.jpg                          # 其他範例圖片
├── IMG-20240321-172354614-AE.jpg     # 範例圖片
└── 2024-07-20-11-26-25.png           # 範例圖片
```

## 🌟 應用場景

- **教育輔助**: 分析教學圖片並回答相關問題
- **圖片說明**: 為圖片生成中文說明
- **內容識別**: 識別圖片中的物體、動物、場景
- **視覺問答**: 針對圖片內容進行問答互動

## 📝 注意事項

- 需要有效的 Google Gemini API 金鑰
- 圖片檔案大小建議在合理範圍內
- 確保圖片格式受 Gemini 支援
- API 使用可能產生費用
- 建議在 Jupyter Notebook 環境中使用以獲得最佳體驗

## 🚀 進階功能

可以擴展為：
- 批次處理多張圖片
- 整合 Web 介面
- 支援影片分析
- 加入語音輸出功能