# JPYExchange - 日圓匯率即時視覺化

## 📖 專案簡介
使用 Python Flask 與 Plotly.js 製作的日圓匯率即時視覺化系統，提供動態匯率數據展示。

## 🛠️ 技術架構
- **後端框架**: Python Flask
- **視覺化函式庫**: Plotly.js
- **前端**: HTML, CSS, JavaScript
- **資料來源**: 匯率 API

## ✨ 主要功能
- 即時日圓匯率查詢
- 動態圖表更新
- 歷史匯率趨勢顯示
- 互動式視覺化介面

## 🚀 安裝與使用

### 環境需求
- Python 3.7+
- Flask
- Plotly
- 匯率資料 API 金鑰（如需要）

### 安裝步驟
1. 安裝相依套件：
   ```bash
   pip install flask plotly requests
   ```

2. 設定 API 金鑰（如使用外部匯率 API）：
   - 註冊匯率資料服務
   - 在程式中設定 API 金鑰

3. 執行應用程式：
   ```bash
   python app.py
   ```

4. 開啟瀏覽器訪問 `http://localhost:5000`

## 📁 檔案結構
```
JPYExchange/
├── README.md
├── app.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    └── js/
```

## 📊 視覺化功能
- 即時匯率折線圖
- 歷史趨勢分析
- 多時間區間切換
- 圖表互動功能

## 📚 學習重點
- Flask 後端開發
- API 資料整合
- Plotly.js 動態圖表
- 即時資料更新
