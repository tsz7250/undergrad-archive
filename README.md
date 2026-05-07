# Two Sum

「Two Sum」是一個經典的程式演算法問題。給定一個整數陣列 `nums` 和一個目標值 `target`，請在該陣列中找出和為目標值 `target` 的那兩個整數，並返回它們的陣列索引。

## 需求說明

### 演算法實作
- **實作兩種方法**:
    - `TwoSumArray()`: 時間複雜度 $O(n \log n)$，空間複雜度 $O(n)$ (用於索引與排序)。
    - `TwoSumHashTable()`: 時間複雜度 $O(n)$，空間複雜度 $O(n)$。
- **複雜度分析**: 清楚記錄每種策略的時間與空間複雜度。
- **程式碼品質**: 撰寫乾淨、模組化且包含良好註解的 C++ 20 程式碼。

### 測試策略
- **全面的測試案例**:
    - **一般案例**: 具有保證解的標準輸入陣列。
    - **邊界案例**: 處理重複數值、負數以及多樣的目標值 (target)。
    - **極限條件**: 最小有效陣列、大範圍數值。
- **測試運行器**: 在 `tests/test_twosum.cpp` 中整合測試套件，驗證所有實作的正確性。

### CI/CD 流程 (GitHub Actions)
- **自動化測試**: 為兩種實作觸發自動化建置與測試。
- **工作流觸發**: 在每次提交 (push) 或拉取請求 (pull request) 到 `main` 分支時執行。

### 軟體打包 (Docker)
- **容器化**: 提供 `Dockerfile` 以實現標準化的環境部署。
- **建置時測試**: 在 Docker 建置過程中包含測試執行步驟，確保僅交付通過驗證的映像檔。

## 建置與執行

### 本機建置
```bash
cmake -B build
cmake --build build
cd build && ctest --output-on-failure
```

### Docker
```bash
docker build -t twosum-solution .
docker run twosum-solution
```

## Github Acitons 的詳述

本專案使用 GitHub Actions 實作完整的持續整合 (CI) 流程。每當有新的程式碼推送到 `main` 分支或建立 Pull Request 時，系統會自動啟動虛擬環境執行以下步驟：

1.  **環境初始化**: 使用 `ubuntu-latest` 映像檔。
2.  **安裝依賴**: 確保系統安裝了最新的 `build-essential` 與 `cmake`。
3.  **編譯驗證**: 透過 CMake 產生建置檔並進行編譯。
4.  **自動測試**: 透過 CTest 執行編譯後的程式，驗證所有 5 個測試案例是否皆通過（包含邊界案例與負數案例）。

### CI 工作流設定

本專案使用 GitHub Actions 進行持續整合，自動化流程定義於 `.github/workflows/ci.yml`，主要運作邏輯如下：

- **自動觸發**：每當程式碼推送 (Push) 或建立拉取請求 (Pull Request) 時，系統會自動啟動建置任務。
- **環境建置**：在標準的 Ubuntu 環境中安裝必要的 C++ 編譯器與 CMake 工具。
- **編譯與測試**：自動執行專案編譯，並隨後透過 CTest 執行完整的測試套件，確保每一項改動都通過正確性驗證。
