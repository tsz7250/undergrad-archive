# MindQuiz_py - Python Flask 心理測驗

## 📖 專案簡介
使用 JavaScript 與 Python Flask 製作的心理測驗系統，結合前後端技術，提供與 MindQuiz 相同的測驗內容但採用伺服器端架構。

## 🛠️ 技術架構
- **後端框架**: Python Flask
- **前端**: HTML, CSS, JavaScript
- **資料處理**: Python + JavaScript
- **架構**: 前後端分離

## ✨ 主要功能
- 伺服器端測驗邏輯
- RESTful API 設計
- 前端與後端資料交互
- 會話狀態管理
- 結果分析處理

## 🚀 安裝與使用

### 環境需求
- Python 3.7+
- Flask
- 現代瀏覽器

### 安裝步驟
1. 安裝 Flask：
   ```bash
   pip install flask
   ```

2. 執行應用程式：
   ```bash
   python app.py
   ```

3. 開啟瀏覽器訪問 `http://localhost:5000`

## 📁 檔案結構
```
MindQuiz_py/
├── README.md
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── data/
    └── questions.json
```

## 🔧 API 端點
- `GET /` - 主頁面
- `GET /api/questions` - 取得測驗題目
- `POST /api/submit` - 提交答案
- `GET /api/result/:id` - 取得測驗結果

## 🎯 技術特色
- **前後端分離**：清楚區分前端展示與後端邏輯
- **API 設計**：RESTful 風格的資料傳輸
- **狀態管理**：伺服器端會話管理
- **資料持久化**：測驗記錄保存

## 📊 與 MindQuiz 比較
| 特性 | MindQuiz (純前端) | MindQuiz_py (Flask) |
|------|------------------|-------------------|
| 技術架構 | 純 JavaScript | Flask + JavaScript |
| 資料處理 | 客戶端 | 伺服器端 |
| 狀態管理 | 前端變數 | Flask Session |
| 資料持久化 | 無 | 可支援資料庫 |

## 📚 學習重點
- Flask 框架使用
- 前後端資料交互
- RESTful API 設計
- 會話管理
- JSON 資料處理
- AJAX 技術應用