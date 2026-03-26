# Acceptance Tests (Validation vs Intended Use)

本文件的驗收準則扣緊 `00_intended_use.md` 中的專案設計目標。此「教育與效能基準測試」專案是否達成開發目的，可透過以下三項主要驗收指標進行確認。

## 1. 驗收準則一：演算法雙重驗證 (Algorithm Cross-Validation)
- **目的**：確認教育用途中對不同策略正確性的展示。
- **操作步驟**：執行由 `tests/test_twosum.cpp` 編譯出的測試執行檔（例如 `./build/tests/test_twosum`）。
- **通過條件**：對於該測試程式中定義的所有測試案例，`TwoSumArray()` ($O(n \log n)$) 與 `TwoSumHashTable()` ($O(n)$) 兩種演算法的輸出結果必須**完全一致**。

## 2. 驗收準則二：持續整合驗證 (Continuous Integration Validation)
- **目的**：確認專案在設定 CI/CD 流程後，能夠作為自動化驗證的參考範例。
- **操作步驟**：在本 repository 已設定 GitHub Actions 工作流程的前提下，將代碼推送 (Push) 至 GitHub repository 的 `main` 分支，以觸發對應的 CI Workflow。
- **通過條件**：若本 repository 已配置 GitHub Actions 工作流程，則該工作流程必須能被成功觸發，並在 `ubuntu-latest` 虛擬環境中依序完成環境部署、代碼編譯並執行測試無誤，最終狀態顯示為綠色的 `Pass`；若尚未配置任何工作流程，則本項視為延伸驗收準則，開發者可自行新增 `.github/workflows/` 中的 CI 設定後再行驗證。

## 3. 驗收準則三：容器化部署驗證 (Containerization Validation)
- **目的**：確認專案在提供 Dockerfile 之後，能夠作為 Docker 環境隔離與封裝的範例。
- **操作步驟**：
  1. 在本 repository 已提供合適的 `Dockerfile` 之後，於本機或測試伺服器執行建立映像檔指令：`docker build -t twosum-test .`
  2. 運行容器：`docker run twosum-test`
- **通過條件**：若已提供對應的 `Dockerfile`，則映像檔必須能夠成功建置且沒有編譯錯誤；容器運行後必須將所有測試結果輸出至標準輸出 (Standard Output)，並且正常結束退出。若目前尚未提供 `Dockerfile`，則本項為可選的延伸驗收準則，開發者可視需求撰寫 `Dockerfile` 後再依上述步驟進行驗證。
