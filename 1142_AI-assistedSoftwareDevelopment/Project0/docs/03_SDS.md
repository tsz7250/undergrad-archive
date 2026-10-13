# SDS — Software Design Specification

## 1. 架構概述 (Architecture Overview)
鑑於本專案為單一的演算法實作，系統架構將直接對應到各個模組檔案上。
互動式示範程式入口為 `src/main.cpp`，主要負責引入其他模組並提供使用者介面；自動化測試與斷言 (Assertions) 則由測試程式 `tests/test_twosum.cpp` 負責執行，而核心演算法則分別獨立於不同的 `.cpp` 與對應的標頭檔 (`.h`) 中。

## 2. 演算法模組設計 (Algorithm Module Design)

### 2.1 排序與雙指標法 (Sorting & Two-Pointers Approach)
- **檔案分類**: `TwoSumArray.cpp`, `TwoSumArray.h`
- **介面簽章**: `std::vector<int> twoSumArray(const std::vector<int>& nums, int target);`
- **運作流程**:
  1. 建立一個包含原陣列值與對應原始索引的結構 (可使用 `std::pair`) 並存入新陣列。
  2. 對該新陣列依數值大小進行遞增排序。
  3. 使用雙指標 (Left 和 Right) 分別指向陣列頭尾，向內逼近直到兩指標所指元素和為 `target`。
- **複雜度分析**:
  - **時間複雜度**: $O(n \log n)$（主要為排序階段的時間消耗，雙指標遍歷為 $O(n)$）。
  - **空間複雜度**: $O(n)$（用於儲存原始索引以供返回正確解答）。

### 2.2 雜湊表法 (Hash Table Approach)
- **檔案分類**: `TwoSumHashTable.cpp`, `TwoSumHashTable.h`
- **介面簽章**: `std::vector<int> twoSumHashTable(const std::vector<int>& nums, int target);`
- **運作流程**:
  1. 建立一個雜湊表 `std::unordered_map<int, int>` 用於記錄掃描過的數值及其索引。
  2. 遍歷一次輸入陣列，對於每一個元素 `nums[i]`，計算差值 `complement = target - nums[i]`。
  3. 若 `complement` 存在於雜湊表中，則找到解答，返回其與當前索引 `i`。若不存在，則將 `nums[i]` 及其索引 `i` 存入雜湊表。
- **複雜度分析**:
  - **時間複雜度**: $O(n)$（只需一次線性遍歷，雜湊表查詢時間期望值為 $O(1)$）。
  - **空間複雜度**: $O(n)$（最差情況下需將全數元素存入雜湊表中）。
