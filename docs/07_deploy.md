# Deployment / Packaging

鑑於本「Two Sum」專案主要作為演算法展示與測試載體，其「部署」概念不同於傳統的 Web 伺服器，而是強調**跨平台的高可攜性 (Portability)** 與**標準化運行環境**。

下述為本專案的兩種標準建置與執行模式：

## 1. 本機原始碼編譯執行 (Local Execution)
開發者可直接於本地端編譯並執行自動化斷言測試 (以 `tests/test_twosum.cpp` 為測試入口)。
- **環境需求**：支援 C++ 20 標準的編譯器 (推薦 `g++` 10.0 以上版本) 與 `cmake`。
- **建置指令**：
  ```bash
  cmake -B build
  cmake --build build
  ```
- **執行指令 (CTest)**：
  ```bash
  cd build && ctest --output-on-failure
  ```

## 2. 持續整合自動化部署 (CI Deployment Automation)
- 本專案已將上述編譯與執行流程，寫入 `.github/workflows/ci.yml`。
- 任何推送到專案分支的動作皆為一次「發布」，GitHub Actions 會自動配置 `ubuntu-latest` 環境建置並運行上述測試，確保專案始終處於完全可用狀態。
