# SRS — Software Requirements Specification

## 1. 功能需求 (Functional Requirements)

### SRS-F001: CSV 檔案解析
系統應能讀取標準 CSV 檔案（逗號分隔、支援引號欄位），並將數據載入至記憶體。支援通過記憶體映射 (Memory-mapped I/O) 優化大檔案讀取效能。

### SRS-F002: 自動雜湊索引建立
資料載入時，系統應自動為所有欄位建立雜湊索引（Hash Index），實現 RowID 與欄位值的映射：`Value -> std::vector<RowID>`。支援精確值匹配查詢。

### SRS-F003: 查詢語法與解析
系統應支援標準 SQL-like 語法：`SELECT ... FROM ... WHERE ...`，包含：
- 基本查詢：`SELECT * FROM data WHERE column = value`
- 複合條件：`AND`、`OR` 邏輯組合
- 例如：`SELECT Name, Age FROM students WHERE Grade = 'A' AND Age < '20'`

### SRS-F004: 複合條件執行引擎
系統應能解析並執行包含 AND/OR 的複雜查詢，透過集合運算（交集、聯集）高效整合多條件結果。

### SRS-F005: 類型推斷
系統應自動識別 CSV 欄位型別（整數、浮點數、字串），並採用適當的比較邏輯與儲存方式。

---

## 2. 效能需求 (Performance Requirements)

### SRS-P001: 精確匹配查詢效率
使用 Hash Index 的精確值查詢應達到 O(1) 時間複雜度。

### SRS-P002: 大檔案支援
系統應支援處理包含數十萬行（即 100,000+ 列）的 CSV 檔案，查詢延遲應在合理範圍內（<100ms）。

### SRS-P003: 記憶體優化
透過記憶體映射技術優化大檔案讀取，減少全檔案載入時的記憶體峰值。

---

## 3. 使用者需求 (User Requirements)

### SRS-U001: 易用的命令列介面
系統應透過命令列接收 CSV 檔案路徑與查詢語句，返回結構化結果。

### SRS-U002: 清晰的輸出格式
查詢結果應以表格或結構化格式（如 CSV、JSON）呈現，易於人工閱讀與機器解析。

---

## 4. 約束與假設 (Constraints & Assumptions)

### SRS-C001: 程式語言與標準
系統使用 C++17 實作，依賴 `csv-parser` 庫進行 CSV 解析。

### SRS-C002: CSV 格式假設
輸入 CSV 應遵循標準格式（逗號分隔、支援引號欄位），首行為列標題。

### SRS-C003: 單機環境
系統設計為單機應用，不涉及分散式或網路查詢。

### SRS-C004: 記憶體限制
系統受限於本機可用記憶體，無法查詢超過記憶體容量的 CSV 檔案。