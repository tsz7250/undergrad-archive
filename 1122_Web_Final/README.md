# 🍽️ 卡利西里餐廳訂餐系統

> ⚠️ **重要聲明**: 這是1122 網站程式設計實務期末專題分組報告作品。專案僅供學習和展示技術實現，菜單內容借用自卡利西里餐廳，純屬教育用途。

一個功能完整的餐廳訂餐系統展示專案，採用現代化Web技術打造，提供直觀的用戶界面和智能化的點餐體驗。本專案作為Web開發技術的學習成果展示。

## 靜態HTML Demo(前端畫面)
**Demo 網址**: [https://tsz7250.github.io/1122_Web_Final/](https://tsz7250.github.io/1122_Web_Final/)
<img src="./pic/index.png" alt="主頁">
<img src="./pic/order.png" alt="直接點餐">
<img src="./pic/chart.png" alt="上月圖表">

## 📋 目錄

- [專案簡介](#專案簡介)
- [主要功能](#主要功能)
- [技術架構](#技術架構)
- [專案結構](#專案結構)
- [系統需求](#系統需求)
- [安裝指南](#安裝指南)
- [設定配置](#設定配置)
- [使用說明](#使用說明)
- [API文件](#api文件)
- [功能截圖](#功能截圖)
- [疑難排解](#疑難排解)
- [授權](#授權)

## 🌟 專案簡介

本專案是一個使用 **Python Flask** 框架開發的餐廳訂餐系統模擬應用程式，作為Web開發技術的學習成果展示。系統整合了多項先進技術，包括人工智慧聊天機器人、數據分析視覺化、以及響應式網頁設計，展示了完整的線上點餐系統開發實作。

### 🎯 專案目標
- 學習和展示現代Web開發技術
- 實作AI整合和數據視覺化功能
- 提供響應式設計的實務經驗
- 完成一個完整的全端開發專案

### 📚 教育目的聲明
- 本專案為學術作品，非商業用途
- 菜單內容參考自卡利西里餐廳，僅供技術展示
- 所有功能均為學習和評估目的而開發

## ✨ 主要功能

### 🍕 點餐功能展示
- **直接點餐**: 瀏覽完整菜單，選擇餐點（展示購物車功能）
- **隨機點餐**: 系統智能推薦功能展示
- **購物車管理**: 即時管理訂單內容和總價計算

### 🤖 AI聊天機器人
- 整合 **Google Gemini AI** 技術
- 智能回答用戶關於餐點的問題
- 提供個性化推薦服務
- 自然語言對話體驗

### 📊 數據分析展示
- **銷售報表**: 視覺化模擬銷售數據
- **PlotlyJS圖表**: 互動式圖表技術展示
- **多維度分析**: 按餐點類型、時間等維度的分析實作

### 🕐 營業管理模擬
- 公休時間設定與顯示功能
- 即時營業狀態更新實作
- 營業時間智能提醒功能

### 🎨 用戶體驗
- **HTML5 Canvas**: 創新的視覺效果
- **響應式設計**: 支援桌面和行動裝置
- **現代化UI**: 美觀的用戶界面設計

## 🔧 技術架構

### 後端技術
- **Python 3.8+**: 主要開發語言
- **Flask 2.0+**: Web應用框架
- **Pandas**: 數據處理和分析
- **LangChain**: AI聊天機器人框架
- **Google Gemini AI**: 自然語言處理

### 前端技術
- **HTML5**: 現代化標記語言
- **CSS3**: 樣式設計和響應式布局
- **JavaScript ES6+**: 動態交互功能
- **PlotlyJS**: 數據視覺化
- **HTML5 Canvas**: 圖形繪製
- **jQuery**: DOM操作和AJAX

### 📄 數據來源說明
- **菜單數據**: 參考卡利西里餐廳真實菜單，僅供學習使用
- **銷售數據**: 模擬數據，用於展示數據分析功能
- **餐廳資訊**: 基於真實餐廳但僅作技術展示用途

### 數據儲存技術
- **JSON**: 菜單和配置數據格式
- **CSV**: 銷售數據分析格式
- **檔案系統**: 靜態資源管理方式

## 📁 專案結構

```
1122_Web_Final/
├── README.md                 # 專案說明文件
├── app.py                   # Flask主應用程式
├── requirements.txt         # Python依賴套件
├── config.ini              # 配置檔案 (需自行建立)
├── 專題報告.pdf             # 專題報告文件
│
├── 核心模組/
│   ├── database_helper.py   # 數據庫操作輔助類
│   ├── llm.py              # AI聊天機器人模組
│   └── sales_helper.py     # 銷售數據分析模組
│
├── templates/              # HTML模板檔案
│   ├── index.html         # 首頁模板
│   ├── order.html         # 點餐頁面模板
│   ├── ordered.html       # 訂單確認模板
│   └── sales.html         # 銷售分析模板
│
└── static/                # 靜態資源目錄
    ├── css/              # 樣式表檔案
    │   ├── index.css
    │   ├── order.css
    │   ├── ordered.css
    │   └── sales.css
    ├── js/               # JavaScript檔案
    │   ├── index.js
    │   ├── order.js
    │   └── sales.js
    ├── images/           # 圖片資源
    │   └── webcanvas.png
    ├── json/             # JSON數據檔案
    │   └── database.json # 餐廳菜單數據
    ├── BillLastMonth.csv # 上月銷售數據
    └── favicon.ico       # 網站圖標
```

## 💻 系統需求

### 基本需求
- **Python**: 3.8 或更高版本

### 必要服務
- **Google Gemini API**: 用於AI聊天機器人功能
- **網路連線**: 用於API調用和外部資源載入

## 🚀 安裝指南

### 1. 複製專案
```bash
git clone https://github.com/tszngaiyip/1122_Web_Final.git
cd 1122_Web_Final
```

### 2. 建立虛擬環境 (建議)
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 4. 設定配置檔案
建立 `config.ini` 檔案 (詳見[設定配置](#設定配置)章節)

### 5. 啟動應用程式
```bash
python app.py
```

### 6. 瀏覽應用程式
在瀏覽器中開啟 `http://localhost:5000`

## ⚙️ 設定配置

### config.ini 配置檔案

在專案根目錄建立 `config.ini` 檔案：

```ini
[Gemini]
API_KEY = your_google_gemini_api_key_here
model = gemini-pro
```

### 取得 Google Gemini API Key

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入您的 Google 帳戶
3. 建立新的 API Key
4. 複製 API Key 到 `config.ini` 檔案

> ⚠️ **安全提醒**: 請勿將 API Key 上傳到公開的版本控制系統

### 環境變數設定 (可選)

```bash
# Windows
set GEMINI_API_KEY=your_api_key_here
set FLASK_ENV=development
```

## 📖 使用說明

### 🏠 首頁功能展示
1. **歡迎界面**: 展示餐廳資訊和主要功能入口
2. **導航選單**: 快速進入各功能頁面
3. **營業狀態**: 即時顯示模擬營業狀態

### 🍽️ 點餐流程展示
1. 點擊「開始點餐」進入點餐頁面
2. 瀏覽不同餐點類別：套餐、麵食、燉飯、漢堡等
3. 選擇餐點加入購物車（模擬功能）
4. 查看訂單詳情和總金額計算
5. 確認訂單並送出（展示完整流程）

### 🎲 隨機點餐功能
1. 選擇「隨機點餐」功能展示
2. 選擇餐點類型或選擇「都可」
3. 系統智能推薦演算法展示
4. 可重新隨機或直接加入訂單

### 💬 AI聊天機器人展示
1. 在點餐頁面找到聊天機器人圖示
2. 輸入關於餐點的問題
3. AI會提供智能回答和推薦（需配置API）
4. 支援自然語言對話技術展示

### 📈 銷售分析功能
1. 點擊「銷售報表」查看數據分析展示
2. 瀏覽互動式圖表技術實作
3. 分析不同餐點類型的銷售模擬數據
4. 查看時間趨勢和熱門餐點分析

## 🔌 API文件

### 餐點相關API

#### 取得隨機餐點
```http
POST /random_pick
Content-Type: application/json

{
    "food_type": "套餐",
    "rand_seed": 12345
}
```

#### 聊天機器人對話
```http
POST /chat
Content-Type: application/json

{
    "message": "推薦一些素食餐點"
}
```

#### 取得銷售數據
```http
GET /sales_data
```

### 回應格式

所有API回應均使用JSON格式：

```json
{
    "success": true,
    "data": {
        // 具體數據內容
    },
    "message": "操作成功"
}
```

## 🖼️ 功能截圖

> 註: 這是學術專題的功能展示截圖

- **首頁界面**: 清晰的導航和營業狀態顯示
- **點餐介面**: 直觀的餐點選擇和購物車功能
- **AI聊天**: 智能對話和推薦介面
- **銷售分析**: 豐富的數據視覺化圖表

## 🛠️ 疑難排解

### 常見問題

#### Q: 無法啟動應用程式，顯示模組找不到錯誤
**A**: 
```bash
# 確認已啟動虛擬環境
pip list  # 檢查已安裝的套件
pip install -r requirements.txt  # 重新安裝依賴
```

#### Q: AI聊天機器人無法回應
**A**: 
1. 檢查 `config.ini` 檔案是否正確設定
2. 確認 API Key 有效且有足夠配額
3. 檢查網路連線狀態

#### Q: 銷售數據無法載入
**A**: 
1. 確認 `static/BillLastMonth.csv` 檔案存在
2. 檢查 CSV 檔案格式是否正確
3. 確認檔案編碼為 UTF-8

#### Q: 靜態檔案無法載入
**A**: 
```bash
# 檢查檔案路徑
ls -la static/css/
ls -la static/js/
ls -la static/images/
```

### 錯誤代碼說明

| 錯誤代碼 | 說明 | 解決方案 |
|---------|------|----------|
| 500 | 伺服器內部錯誤 | 檢查應用程式日誌 |
| 404 | 檔案或路由不存在 | 確認URL路徑正確 |
| 400 | 請求格式錯誤 | 檢查API請求格式 |

### 日誌查看

應用程式日誌會顯示在終端機中，如需詳細除錯：

```bash
# 啟用除錯模式
export FLASK_DEBUG=1
python app.py
```

### 新增功能

1. 在 `app.py` 中新增路由
2. 建立對應的 HTML 模板
3. 新增必要的 CSS 和 JavaScript
4. 更新 README 文件

## 📄 授權

此專案為學術期末專題作品，僅供教育和學習用途。

### 📝 特別聲明
- 本專案非商業用途，純屬學術展示
- 菜單內容參考自卡利西里餐廳，僅供技術實作學習
- 如有侵權請聯繫，將立即移除相關內容
- 感謝卡利西里餐廳提供優質菜單內容作為學習參考

此專案僅供學習和教育用途。