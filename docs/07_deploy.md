# Deployment / Packaging

---

## 1. 環境要求

| 項目 | 要求 | 備註 |
|-----|------|------|
| **作業系統** | Linux / macOS / Windows | 透過 CMake 跨平台支援 |
| **C++ 編譯器** | GCC 7.0+ / Clang 5.0+ / MSVC 2017+ | C++17 支援 |
| **CMake** | 3.10+ | 構建系統 |
| **vcpkg** | 最新版本 | 套件管理 |
| **記憶體** | 2GB+ | 建議用於測試 1M 行 CSV |
| **磁碟空間** | 500MB+ | 依賴庫 + 構建產物 |

---

## 2. 本機部署步驟

### 步驟 1：安裝依賴
```bash
# 使用 vcpkg 安裝所需庫
vcpkg install csv-parser gtest

# 設定環境變數（如未自動設置）
export VCPKG_ROOT=/path/to/vcpkg
```

### 步驟 2：克隆或下載專案
```bash
git clone <repository_url>
cd 11402_CS351_ProjectB
```

### 步驟 3：構建專案
```bash
# 建立構建目錄
mkdir build && cd build

# 使用 CMake 配置（指定 vcpkg toolchain）
cmake .. -DCMAKE_TOOLCHAIN_FILE=${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake -DCMAKE_BUILD_TYPE=Release

# 編譯
make -j4
```

### 步驟 4：執行與驗證
```bash
# 執行主程式（需傳入 CSV 檔案路徑和查詢語句）
./bin/csv_db_engine <csv_file> "<query_string>"

# 例如
./bin/csv_db_engine data/students.csv "SELECT * FROM students WHERE Grade = 'A'"
```

### 步驟 5：執行測試
```bash
# 運行單元測試
ctest --verbose

# 或直接執行測試二進位檔
./bin/test_csv_parser
./bin/test_hash_index
./bin/test_query_engine
```

---

## 3. Docker 容器部署

### 步驟 1：構建 Docker 映像
```bash
# 在專案根目錄執行（Dockerfile 應存在）
docker build -t csv-db-engine:latest .
```

### 步驟 2：運行容器
```bash
# 互動式運行
docker run -it csv-db-engine:latest

# 綁定本機資料卷（便於輸入 CSV 檔案）
docker run -it -v /path/to/local/data:/data csv-db-engine:latest
```

### 步驟 3：在容器中執行
```bash
# 在容器內
/app/bin/csv_db_engine /data/students.csv "SELECT * FROM students WHERE Grade = 'A'"
```

---

## 4. 已知限制與工作區

### 限制 1：CSV 格式假設
- 系統假設 CSV 為標準格式（逗號分隔、支援引號欄位）
- 不支援自訂分隔符（如制表符、分號）
- 首行必須為列標題

### 限制 2：記憶體上限
- 系統受本機可用記憶體限制
- 建議單個 CSV 檔案不超過 100GB
- 對於更大檔案，考慮分片處理

### 限制 3：查詢語法範圍
- 支援 `SELECT ... FROM ... WHERE ...` 基本語法
- 不支援 `JOIN`、`GROUP BY`、`HAVING` 等進階 SQL 功能
- WHERE 條件限制為兩層嵌套（AND/OR 組合）

### 限制 4：單機部署
- 系統設計為單機應用
- 不支援分散式查詢或多機部署

---

## 5. 故障排除

### 問題 1：CMake 找不到 vcpkg Toolchain
**症狀**：構建時出現 `vcpkg.cmake not found` 錯誤  
**解決方案**：
```bash
# 確認 VCPKG_ROOT 環境變數正確
echo $VCPKG_ROOT

# 重新執行 CMake，明確指定路徑
cmake .. -DCMAKE_TOOLCHAIN_FILE=<absolute_path_to_vcpkg.cmake>
```

---

### 問題 2：CSV 解析失敗或結果為空
**症狀**：程式執行無誤但沒有輸出  
**解決方案**：
1. 驗證 CSV 檔案格式（逗號分隔、首行為標題）
2. 檢查檔案編碼（應為 UTF-8）
3. 檢查查詢語法是否正確
```bash
# 調試：查看解析後的行數
./bin/csv_db_engine <csv_file> "SELECT COUNT(*)"
```

---

### 問題 3：查詢超時或記憶體不足
**症狀**：大 CSV 檔案查詢卡頓或應用崩潰  
**解決方案**：
- 縮小 CSV 檔案或分片處理
- 使用更精確的查詢條件，減少結果集
- 增加系統可用記憶體或在記憶體更大的機器上運行

---

### 問題 4：Docker 容器啟動失敗
**症狀**：`docker run` 出現錯誤  
**解決方案**：
```bash
# 查看容器構建日誌
docker build -t csv-db-engine:latest . --no-cache

# 驗證 Dockerfile 完整性
# 檢查容器執行日誌
docker logs <container_id>
```

---

## 6. 效能調整

### 編譯優化
```bash
# 發行版構建（推薦用於生產）
cmake .. -DCMAKE_BUILD_TYPE=Release -O3

# 調試版構建（用於開發與問題排查）
cmake .. -DCMAKE_BUILD_TYPE=Debug -g
```

### 記憶體優化
- 使用記憶體映射 I/O（csv-parser 預設啟用）
- 對大 CSV 檔案進行分片處理
- 考慮定期清空結果集以釋放記憶體

---

## 7. 版本與相容性

| 版本 | 發佈日期 | 備註 |
|------|---------|------|
| 0.1.0 | 2024 年 4 月 | 初始版本，基本功能完備 |
| 0.1.1+ | TBD | 效能最佳化、缺陷修復 |

---

## 8. 支援與反饋

- **缺陷報告**：提交至 GitHub Issues
- **功能建議**：提交至 GitHub Discussions
- **技術支援**：聯絡專案維護者