# Steiner Trees Algorithm
## 史坦納樹演算法實作

### 專案描述 (Project Description)
本程式使用 RISC-V 組合語言實作史坦納樹（Steiner Tree）演算法，計算連接給定點集的最小樹。

This program implements the Steiner Tree algorithm using RISC-V assembly language to find the minimum tree connecting a given set of points.

### 功能特色 (Features)
- **座標點處理** - 處理二維座標點集
- **最小樹計算** - 計算連接所有點的最小史坦納樹
- **格式化輸出** - 輸出樹的邊連接資訊

### 檔案說明 (Files)
- `s1111452_HW3.asm` - RISC-V 組合語言主程式
- `s1111452_HW3_demo.png` - 程式執行結果示例
- `README.md` - 本說明文件

### 輸入限制 (Input Constraints)
1. **節點數量限制** - 圖形節點數不超過 9 個
2. **座標範圍限制** - X 和 Y 座標僅限 0-9 之間的整數

### 輸入格式 (Input Format)
```
PointsNumber,Point1_X,Point1_Y,Point2_X,Point2_Y,…
```
- `PointsNumber` - 點的總數
- `Point1_X,Point1_Y` - 第一個點的 X, Y 座標
- 依此類推...

### 輸出格式 (Output Format)
```
PointStart1_X,PointStart1_Y,PointEnd1_X,PointEnd1_Y
PointStart2_X,PointStart2_Y,PointEnd2_X,PointEnd2_Y
PointStart3_X,PointStart3_Y,PointEnd3_X,PointEnd3_Y
...
```
每行代表史坦納樹中的一條邊，從起始點到終點的座標。

### 使用方式 (Usage)
1. 使用 RISC-V 模擬器載入 `.asm` 檔案
2. 依照指定格式輸入點座標資料
3. 程式將計算並輸出史坦納樹的邊連接資訊

### 執行結果 (Demo)
請參考 `s1111452_HW3_demo.png` 查看程式執行範例。

