# Known Issues / Limitations

在針對本專案進行 `tests/test_twosum.cpp` 的測試驗證後，發現下列已知問題或潛在限制：

1. **編譯標準支援問題 (`c++20` vs `c++2a`)**
   - 根據 `README.md`，專案建議使用 `g++ -std=c++20` 編譯。但是在某些較舊版本的 GCC 環境下，會出現 `unrecognized command line option '-std=c++20'` 的錯誤。
   - **解決/緩解方案**：在這類環境下，可將編譯參數退回改用 `-std=c++2a`。GitHub Actions 的 `ubuntu-latest` 環境中預設含有較新版的 GCC，依然能正常支援 `-std=c++20`。

2. **演算法多重解的順序一致性**
   - 雖然 `04_test_plan.md` 的測試案例（一般案例、負數、包含重複值等）在兩套演算法 `TwoSumArray()` ($O(n \log n)$) 與 `TwoSumHashTable()` ($O(n)$) 的執行下，得出了**完全一致**的答案（均順利通過測試），但理論上當輸入陣列中包含多組符合目標的配對時，這兩種演算法（因掃描機制與排序後影響）有可能會返回不同的目標索引。這點在目前的測試計畫中尚未產生問題，因為目前設定的測資皆只有唯一解。