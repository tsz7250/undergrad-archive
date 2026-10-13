# Test Plan (Verification)

## 1. 測試策略 (Test Strategy)
由於本專案主要為單純的演算法實踐，測試策略將以「白箱與黑箱單元測試」為主，所有的測試案例都會在 `tests/test_twosum.cpp` 中以斷言 (Assertions) 形式實作。當有任何一項測試失敗時，程式應以非零狀態碼 (Non-zero exit code) 退出，以利整合進 CI 流程。

## 2. 測試範圍覆蓋 (Test Coverage)

### 2.1 一般情況 (Normal Cases)
- **測試案例 1**：陣列包含唯一的解答組，數值皆為正整數且無重複。
  - 輸入範例: `nums = [2, 7, 11, 15], target = 9`
  - 預期輸出: `[0, 1]`

### 2.2 特殊與邊界情況 (Edge & Special Cases)
- **測試案例 2 (負數)**：輸入陣列包含負數及正數。
  - 輸入範例: `nums = [-3, 4, 3, 90], target = 0`
  - 預期輸出: `[0, 2]`
- **測試案例 3 (重複數值)**：輸入陣列中包含解為完全相同的兩個數字。
  - 輸入範例: `nums = [3, 3], target = 6`
  - 預期輸出: `[0, 1]`
- **測試案例 4 (無解)**：陣列中無任何兩數能加總為目標值。
  - 輸入範例: `nums = [1, 2, 3], target = 7`
  - 預期輸出: `[]` (空陣列)

### 2.3 效能測試 (Performance Cases)
- **測試案例 5 (動態大規模測試)**：為了突顯 `TwoSumHashTable` ($O(n)$) 與 `TwoSumArray` ($O(n \log n)$) 的時間複雜度差異，程式會於執行期間動態生成大量元素的陣列（如 $10,000$ 與 $100,000$ 個元素），並將目標值設定為無法找到的狀態（最差情況）。使用 `<chrono>` 函式庫精確測量雙方的執行時間，並輸出於終端機進行比對。

## 3. 自動化測試腳本 (Automation)
本專案的測試將透過 GitHub Actions 自動執行。每次觸發 `Push` 或 `Pull Request` 時，系統會：
1. 配置與編譯專案：使用 `cmake -B build` 配置並以 `cmake --build build` 進行編譯。
2. 執行測試：使用 `ctest` 指令（於 `build` 目錄下執行 `ctest --output-on-failure`）或直接執行生成的 `test_twosum` 執行檔。
3. 判定結果：若 `ctest` 回報測試通過或執行檔輸出狀態碼為 `0`，則表示所有單元測試通過；若失敗，CI 流程將會標示為失敗 (Failed)。
