# SimpleRPG+LLM - 結合 LLM 的 RPG 遊戲

## 📖 專案簡介
在 SimpleRPG 的基礎上整合大型語言模型(LLM)，為 RPG 遊戲添加智能對話系統，讓 NPC 具有更豐富的互動性與隨機性。

## 🛠️ 技術架構
- **遊戲引擎**: JavaScript (基於 SimpleRPG)
- **AI 服務**: 大型語言模型 API
- **後端**: Python Flask (處理 AI 請求)
- **前端**: HTML5 Canvas, CSS, JavaScript

## ✨ 新增功能
- **角色扮演設定**：可為 NPC 設定具體的角色身份
- **智能對話**：NPC 回應具有隨機性與情境感知
- **動態劇情**：根據對話發展產生不同的故事走向
- **個性化互動**：每個 NPC 都有獨特的對話風格

## 🚀 安裝與使用

### 環境需求
- Python 3.7+
- Flask
- LLM API 金鑰（如 OpenAI, Google Gemini 等）
- 現代瀏覽器

### 安裝步驟
1. 安裝 Python 相依套件：
   ```bash
   pip install flask requests openai
   ```

2. 設定 LLM API 金鑰：
   - 在 `config.py` 中設定 API 金鑰
   - 選擇適合的 LLM 服務

3. 啟動後端服務：
   ```bash
   python app.py
   ```

4. 開啟 `index.html` 開始遊戲

## 📁 檔案結構
```
SimpleRPG+LLM/
├── README.md
├── index.html
├── app.py                 # Flask 後端
├── config.py             # API 設定
├── js/
│   ├── game.js
│   ├── player.js
│   ├── ai_dialogue.js    # AI 對話系統
│   └── llm_integration.js
├── css/
│   └── style.css
├── images/
│   └── (遊戲圖像資源)
└── data/
    ├── npcs.json         # NPC 角色設定
    └── dialogue_templates.json
```

## 🤖 AI 對話系統

### 角色扮演設定
- 每個 NPC 都有預設的角色背景
- 包含性格特質、職業、背景故事
- 可自定義角色設定檔

### 隨機性實現
- 每次對話都有不同的回應
- 基於上下文的智能回覆
- 情境感知的對話內容

## 🎮 遊戲體驗

### 基礎功能（繼承自 SimpleRPG）
- 角色移動與碰撞偵測
- 地圖探索
- 終點目標

### AI 增強功能
- **智能 NPC**：與 NPC 對話獲得隨機且有意義的回應
- **動態故事**：每次遊戲都有不同的故事發展
- **個性化體驗**：AI 會記住玩家的選擇與行為

## 🔧 API 整合

### 支援的 LLM 服務
- OpenAI GPT 系列
- Google Gemini
- Anthropic Claude
- 其他相容的 LLM API

### 對話流程
1. 玩家與 NPC 互動
2. 前端發送對話請求到 Flask 後端
3. 後端調用 LLM API 生成回應
4. 回應傳回前端並顯示給玩家

## 📚 學習重點
- LLM API 整合技術
- 前後端資料交互
- 角色扮演系統設計
- 遊戲 AI 應用
- 自然語言處理
- 即時對話系統

## 🎯 與 SimpleRPG 比較
| 功能 | SimpleRPG | SimpleRPG+LLM |
|------|-----------|---------------|
| 基礎移動 | ✓ | ✓ |
| 碰撞偵測 | ✓ | ✓ |
| 終點判斷 | ✓ | ✓ |
| NPC 對話 | 靜態文字 | AI 動態生成 |
| 角色設定 | 無 | 詳細角色背景 |
| 對話隨機性 | 無 | 每次都不同 |

## ⚠️ 注意事項
- 需要穩定的網路連線使用 LLM API
- API 調用會產生費用
- 對話內容可能因 AI 模型而異
- 建議設定適當的內容過濾機制
