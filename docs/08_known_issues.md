# Known Issues / Limitations

## ✅ 測試執行結果 (2026-04-13 已修復)

**最終測試通過率**: 55/55 (100%) ✅

### 最終測試統計
- **總測試數**: 55
- **通過**: 55 ✅
- **失敗**: 0

---

## ✅ 已修復的測試失敗問題

### 1. CSVParserTest.EmptyFile (已修復 ✅)
**狀態**: 完成  

**原問題**:
```
test_csv_parser.cpp(98): error: Expected: parser.parseFile(filename) throws 
an exception of type std::runtime_error.
Actual: it throws nothing.
```

**根本原因**:
csv_parser.cpp 在解析空 CSV 文件時直接返回空結果，而不拋出異常。

**修復方案** (已實施):
在 csv_parser.cpp 第 24-27 行修改空文件處理邏輯，現在拋出 `std::runtime_error("Empty CSV file: " + file_path)`。

**修改前**:
```cpp
if (!std::getline(file, line)) {
    if (file.eof()) {
        // Empty file
        return rows;  // ❌ 直接返回
    }
    throw std::runtime_error("Failed to read header from file: " + file_path);
}
```

**修改後**:
```cpp
if (!std::getline(file, line)) {
    if (file.eof()) {
        // Empty file - throw exception
        throw std::runtime_error("Empty CSV file: " + file_path);  // ✅ 現在拋出異常
    }
    throw std::runtime_error("Failed to read header from file: " + file_path);
}
```

---

### 2. QueryParserTest.ParseComparisonOperators (已修復 ✅)
**狀態**: 完成  

**原問題**:
```
C++ exception with description "Query parse error: Expected comparison operator, 
got: ! at token: !" thrown in the test body.
```

**根本原因**:
query_parser.cpp 的 tokenize() 函數中，條件 `else if (c == '=' || c == '<' || c == '>')` 沒有包括 '!' 字符。雖然代碼內部有處理 "!=" 的邏輯，但 '!' 永遠不會進入該條件分支，導致被作為一般字符處理。

**修復方案** (已實施):
修改 query_parser.cpp 第 61 行的條件，添加 `|| c == '!'`  

**修改前**:
```cpp
} else if (c == '=' || c == '<' || c == '>') {  // ❌ 缺少 '!'
    // ... 處理多字符運算符
    } else if (c == '!' && i + 1 < query_str.length() &&
               query_str[i + 1] == '=') {
        tokens_.push_back("!=");
        i++;
    }
```

**修改後**:
```cpp
} else if (c == '=' || c == '<' || c == '>' || c == '!') {  // ✅ 添加了 '!'
    // ... 處理多字符運算符
    } else if (c == '!' && i + 1 < query_str.length() &&
               query_str[i + 1] == '=') {
        tokens_.push_back("!=");
        i++;
    }
```

---

## 📋 變更歷史

| 日期 | 測試 | 狀態 | 修改 |
|------|------|------|------|
| 2026-04-13 | CSVParserTest.EmptyFile | ✅ 修復 | 添加異常拋出 |
| 2026-04-13 | QueryParserTest.ParseComparisonOperators | ✅ 修復 | 修復 tokenize() 條件 |

---

## 🛠️ 後續改進建議

1. **代碼審查**: 
   - 檢查是否還有其他隱藏的 tokenize() 字符處理遺漏

2. **文件驗證**:
   - 考慮添加 CSV 文件格式驗證
   - 確定是否應允許只含標題行的 CSV 文件

3. **運算符擴展**:
   - 如果需要，可考慮添加更多比較運算符 (如 LIKE、IN 等)

4. **持續集成**:
   - 建立自動化測試流程確保未來的變更不會破壞現有功能