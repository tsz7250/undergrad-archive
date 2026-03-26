# Deployment / Packaging

鑑於本「Two Sum」專案主要作為演算法展示與測試載體，其「部署」概念不同於傳統的 Web 伺服器，而是強調**跨平台的高可攜性 (Portability)** 與**標準化運行環境**。

下述為本專案的兩種標準建置與執行模式：

## 1. 本機原始碼編譯執行 (Local Execution)
開發者可直接於本地端編譯並執行自動化斷言測試。
- **環境需求**：支援 C++ 20 標準的編譯器 (推薦 `g++` 10.0 以上版本)。
- **建置指令**：
  ```bash
  g++ -std=c++20 main.cpp TwoSumArray.cpp TwoSumHashTable.cpp -o solution
  ```
- **執行指令**：
  ```bash
  ./solution
  ```
- **預期結果**：程式安靜退出 (Exit code 0)，代表所有內建測試案例皆通過。

## 2. 容器化封裝與運行 (Docker Containerization)
為了消除作業系統與編譯器版本的差異，本專案提供 `Dockerfile` 進行環境封裝。
- **環境需求**：必須安裝 Docker Engine。
- **建置 Docker 映像檔**：
  此步驟不僅會封裝代碼，也會在容器內部環境進行 `g++` 編譯。
  ```bash
  docker build -t twosum-solution .
  ```
- **執行測試容器**：
  執行已編譯完成的映像檔，立即得出測試運行結果。
  ```bash
  docker run twosum-solution
  ```

## 3. 持續整合自動化部署 (CI Deployment Automation)
- 本專案已將上述編譯與執行流程，寫入 `.github/workflows/test.yml`。
- 任何推送到 `main` 分支的動作皆為一次「發布」，GitHub Actions 會自動配置 `ubuntu-latest` 環境建置並運行上述測試，確保主分支永遠處於完全可用狀態。
