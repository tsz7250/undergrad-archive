# SRS — Software Requirements Specification

## 1. 簡介 (Introduction)
本文件定義了「Two Sum」專案的軟體需求。本專案為一個演算法教育與 CI/CD 示範工具，旨在提供兩種不同時間複雜度 ($O(n \log n)$ 與 $O(n)$) 的 Two Sum 問題解法，並透過單元測試與 Docker 容器化進行驗證。

## 2. 功能性需求 (Functional Requirements)
- **FR-01 (基本運算)**：系統必須能夠接收一個整數陣列 `nums` 與一個目標整數 `target`，並回傳陣列中兩個相加等於 `target` 的元素索引。
- **FR-02 (邊界處理)**：系統必須能夠正確處理包含負數、重複數值的陣列輸入。
- **FR-03 (無解處理)**：若陣列中不存在符合條件的解，系統應能合法且明確地表示（例如回傳空陣列）。
- **FR-04 (雙重實作)**：系統必須提供兩種不同的演算法實作 (`TwoSumArray` 與 `TwoSumHashTable`)。

## 3. 非功能性需求 (Non-Functional Requirements)
- **NFR-01 (效能指標 - 方法 A)**：其中一種實作的時間複雜度必須限制在 $O(n \log n)$ 內，空間複雜度 $O(n)$ 以下。
- **NFR-02 (效能指標 - 方法 B)**：另一種實作的時間複雜度必須達到 $O(n)$，允許使用額外空間至 $O(n)$。
- **NFR-03 (編譯標準)**：所有的程式碼必須完全相容並使用 C++ 20 標準進行編譯。
- **NFR-04 (自動化驗證)**：專案必須整合 GitHub Actions，在每次推送至 `main` 分支時自動觸發建置與測試。
