# SDS — Software Design Specification

## 1. 系統架構 (System Architecture)

```
┌─────────────┐
│  CSV File   │
└──────┬──────┘
       │ Parsing (csv-parser)
       ▼
┌──────────────────────┐
│  Storage Layer       │
│  (In-Memory Rows)    │
└──────┬───────────────┘
       │ Automatic Indexing
       ▼
┌──────────────────────┐
│  Hash Index Layer    │
│  Value -> RowID[]    │
└──────┬───────────────┘
       │
┌──────────────────────┐
│  Query String        │
└──────┬───────────────┘
       │ Parsing & Tokenization
       ▼
┌──────────────────────┐
│  Query Parser        │
│  -> AST / Tokens     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Execution Engine    │
│  Lookup + Set Ops    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Result Set          │
└──────────────────────┘
```

---

## 2. 主要模組設計 (Module Design)

### SDS-M001: CSV Parser Module
**責任**：讀取 CSV 檔案、解析行與列、處理引號與轉義。
**輸入**：檔案路徑  
**輸出**：`std::vector<std::map<std::string, std::string>>`（每行一個 map，key 為欄名，value 為欄值）  
**依賴**：`csv-parser` 庫

### SDS-M002: Storage Layer
**責任**：將解析後的數據存儲在記憶體中，賦予每行唯一 RowID。
**輸入**：Parser 輸出  
**輸出**：
- `std::vector<std::map<std::string, std::string>> data`（按 RowID 索引的行資料）
- `std::vector<std::string> columns`（欄名清單）

**實作細節**：
```cpp
struct Row {
    RowID id;
    std::map<std::string, std::string> values;
};
std::vector<Row> rows;
```

### SDS-M003: Hash Index Builder
**責任**：為每個欄位建立雜湊索引，支援精確值查詢。
**輸入**：Storage Layer 數據  
**輸出**：`std::map<std::string, std::map<std::string, std::vector<RowID>>>`
- 第一層 key：欄名  
- 第二層 key：欄值  
- value：包含該值的 RowID 清單

**時間複雜度**：O(n*m)，n 為行數，m 為平均欄數

### SDS-M004: Query Parser
**責任**：解析 SQL-like 查詢字符串，生成抽象語法樹 (AST)。
**輸入**：查詢字符串，例如 `"SELECT Name, Age FROM data WHERE Grade = 'A' AND Age < '20'"`  
**輸出**：AST 結構，包含：
- 選擇欄位清單
- WHERE 條件樹（支援 AND/OR）
- 比較運算子（=, <, >, <=, >=, !=）

**實作細節**：遞迴下降解析器 (Recursive Descent Parser)

### SDS-M005: Query Execution Engine
**責任**：根據 AST 執行查詢，透過索引快速查找與集合運算。
**流程**：
1. 解析 WHERE 條件
2. 對於每個簡單條件，透過 Hash Index 查找符合的 RowID 集合
3. 透過 AND 運算（交集）或 OR 運算（聯集）合併多條件結果
4. 根據選擇欄位清單提取結果集

**時間複雜度**：O(log n + k)，n 為行數，k 為結果集大小

---

## 3. 主要數據結構

### RowID
```cpp
using RowID = size_t;  // 行的唯一標識符
```

### Hash Index 結構
```cpp
std::map<std::string, std::map<std::string, std::vector<RowID>>> index;
// index[column][value] = {rowid1, rowid2, ...}
```

### AST 節點（簡化）
```cpp
struct ASTNode {
    enum Type { Leaf, AND, OR } type;
    std::string column;      // 僅用於 Leaf
    std::string op;          // 比較運算子, 僅用於 Leaf
    std::string value;       // 欄值, 僅用於 Leaf
    ASTNode* left;
    ASTNode* right;
};
```

---

## 4. 典型執行流程

**場景**：`SELECT Name FROM students WHERE Grade = 'A' AND ID = '123'`

1. **CSV 載入**：讀取 students.csv，建立 Storage Layer
2. **索引建立**：為 Grade、ID 等所有欄位建立 Hash Index
3. **查詢解析**：
   - 選擇欄位：Name
   - WHERE 條件：`Grade = 'A' AND ID = '123'`
4. **執行**：
   - 查找 `index["Grade"]["A"]` → {rid1, rid2, ...}
   - 查找 `index["ID"]["123"]` → {rid_k}
   - 交集運算 → {rid_target}
5. **提取結果**：返回 rid_target 對應的 Name 值

---

## 5. 設計決策

- **記憶體映射**：CSV 解析時使用 csv-parser 庫的內置優化，而非手動實作。
- **Hash Index 粒度**：為所有欄位建立索引，確保任何查詢都能利用快速查找。
- **AST 設計**：簡化版本，支援二元運算子（AND/OR），便於遞迴執行與優化。