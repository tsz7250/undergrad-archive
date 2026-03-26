# Traceability Matrix

本矩陣用於追溯需求 (SRS)、設計 (SDS) 與測試驗證 (Test Plan, Acceptance Tests) 之間的對應關係，確保專案的所有功能與非功能性目標皆已被實作與測試涵蓋。

| 需求 ID (SRS) | 需求簡述 | 對應設計模組 (SDS) | 對應測試案例 (Test Plan) | 備註說明 |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | 基本運算（找尋總和） | `TwoSumArray`, `TwoSumHashTable` | 案例 1 (一般情況) | 在 `main.cpp` 中以 Assertions 驗證。 |
| **FR-02** | 邊界處理（負數、重複值） | `TwoSumArray`, `TwoSumHashTable` | 案例 2, 3 (負數與重複數值) | |
| **FR-03** | 無解處理 | `TwoSumArray`, `TwoSumHashTable` | 案例 4 (無解) | 回傳應為空陣列。 |
| **FR-04** | 雙重實作演算法 | 架構概述 (兩種方法) | 驗收準則一 (保證一致性) | 驗證兩者針對相同輸入結果必定相同。 |
| **NFR-01** | $O(n \log n)$ 效能要求 | 排序與雙指標法模組 | 驗收準則一 | 確保 `TwoSumArray.cpp` 邏輯符合指標。 |
| **NFR-02** | $O(n)$ 效能要求 | 雜湊表法模組 | 驗收準則一 | 確保 `TwoSumHashTable.cpp` 邏輯符合指標。 |
| **NFR-03** | C++ 20 標準相容 | 架構概述, `.github/workflows/test.yml` | 驗收準則二 (CI 編譯) | 於 `g++ -std=c++20` 參數下建置。 |
| **NFR-04** | 自動化 CI/CD 驗證 | `07_deploy.md` 部署定義 | 驗收準則二, 驗收準則三 | GitHub Actions 及 Docker Build 測試。 |
