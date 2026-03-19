# Project Plan (Jira + Git Workflow)

## 開發流程 (Development Workflow)
專案採用典型的 **Git Flow** 工作流，確保代碼品質與穩定性：
- **main 分支**：存放穩定、隨時可交付的產品代碼。
- **feature/* 分支**：每個新功能或演算法實作都在獨立的分支進行開發。
- **Pull Request (PR)**：所有變更必須通過代碼審查與 CI 管道驗證後，方能併入 main 分支。

## 專案階段 (Project Phases)

### 第一階段：基礎演算法實作 (Milestone 1)
- 實作 `$O(n \log n)$` 之 `TwoSumArray()` 函式。
- 建立主程式 `main.cpp` 用於運行基本測試案例。

### 第二階段：優化演算法實作 (Milestone 2)
- 實作 `$O(n)$` 之 `TwoSumHashTable()` 函式。
- 更新測試套件，確保兩種實作的結果一致且正確。

### 第三階段：持續整合與自動化測試 (Milestone 3)
- 配置 GitHub Actions 工作流。
- 實作自動化測試腳本，涵蓋邊界案例、負數案例及極限狀況。

### 第四階段：容器化與部署 (Milestone 4)
- 撰寫 `Dockerfile`，配置標準化的編譯與執行環境。
- 驗證 Docker 環境下的效能與輸出正確性。

## 任務追蹤 (Task Tracking)
本專案整合 **Jira** 進行專案管理：
- 每項功能與錯誤修復將對應一個 Jira Ticket。
- Git 提交訊息應包含對應的 Jira Issue ID（例如：`[PROJ-123] Implement hash table approach`）。
- 開發者需定期更新 Jira 看板上的狀態（To Do -> In Progress -> Review -> Done）。
