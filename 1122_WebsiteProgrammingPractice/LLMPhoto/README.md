# LLMPhoto - LLM 圖片理解服務

## 📖 專案簡介
使用 Google Gemini AI 製作的圖片理解服務，能夠分析上傳的圖片並提供智能描述與解析。

## 🛠️ 技術架構
- **AI 服務**: Google Gemini Vision API
- **後端**: Python Flask
- **前端**: HTML, CSS, JavaScript
- **圖片處理**: PIL/Pillow

## ✨ 主要功能
- 圖片上傳功能
- AI 圖片內容分析
- 智能描述生成
- 多語言支援
- 即時結果顯示

## 🚀 安裝與使用

### 環境需求
- Python 3.7+
- Flask
- Google Gemini API 金鑰
- PIL/Pillow

### 安裝步驟
1. 安裝相依套件：
   ```bash
   pip install flask google-generativeai pillow
   ```

2. 設定 API 金鑰：
   - 取得 Google Gemini API 金鑰
   - 在程式中設定 API 金鑰

3. 執行應用程式：
   ```bash
   python app.py
   ```

4. 開啟瀏覽器訪問 `http://localhost:5000`

## 📁 檔案結構
```
LLMPhoto/
├── README.md
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
└── requirements.txt
```

## 🔧 功能特色
- 支援多種圖片格式（JPG, PNG, GIF 等）
- 智能內容識別
- 物件偵測與描述
- 場景理解
- 文字識別（OCR）

## 📚 學習重點
- Google Gemini Vision API 使用
- 圖片處理技術
- AI 視覺理解
- 檔案上傳處理
- Flask 應用開發
