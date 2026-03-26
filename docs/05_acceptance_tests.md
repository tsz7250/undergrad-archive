# Acceptance Tests (Validation vs Intended Use)

本文件的驗收準則扣緊 `00_intended_use.md` 中的專案設計目標。此「教育與效能基準測試」專案是否達成開發目的，可透過以下三項主要驗收指標進行確認。

## 1. 驗收準則一：演算法雙重驗證 (Algorithm Cross-Validation)
- **目的**：確認教育用途中對不同策略正確性的展示。
- **操作步驟**：執行編譯後的主應用程式。
- **通過條件**：對於所有定義的測試案例，`TwoSumArray()` ($O(n \log n)$) 與 `TwoSumHashTable()` ($O(n)$) 兩種演算法的輸出結果必須**完全一致**。

## 2. 驗收準則二：持續整合驗證 (Continuous Integration Validation)
- **目的**：確認專案能夠作為 CI/CD 流程的參考範例。
- **操作步驟**：將代碼推送 (Push) 至 GitHub repository 的 `main` 分支。
- **通過條件**：GitHub Actions 工作流程 (CI Workflow) 必須能被成功觸發，並在 `ubuntu-latest` 虛擬環境中依序完成環境部署、代碼編譯並執行測試無誤，最終狀態顯示為綠色的 `Pass`。

## 3. 驗收準則三：容器化部署驗證 (Containerization Validation)
- **目的**：確認專案能夠作為 Docker 環境隔離與封裝的範例。
- **操作步驟**：
  1. 於本機或測試伺服器執行建立映像檔指令：`docker build -t twosum-test .`
  2. 運行容器：`docker run twosum-test`
- **通過條件**：映像檔必須能夠成功建置且沒有編譯錯誤；容器運行後必須將所有測試結果輸出至標準輸出 (Standard Output)，並且正常結束退出。
