# Project Plan (Jira + Git Workflow)

## 開發流程 (Development Workflow)
本專案採用 Git Workflow，結合 Jira 進行任務管理與追蹤。開發流程包含：

1. 需求與任務分解：於 Jira 上建立 User Story 與 Task。
2. 分支管理：每項功能或修正以 feature/ 或 bugfix/ 分支開發，主分支為 main。
3. Pull Request 與 Code Review：功能完成後發送 PR，經團隊審查後合併。
4. 持續整合（CI）：每次提交自動執行單元測試與 Linter 校驗，確保品質。

## 專案階段 (Project Phases)
1. 需求分析（SRS 文件）
2. 系統設計（SDS 文件）
3. 程式實作（含 CSV 解析、索引、查詢引擎等模組）
4. 單元與壓力測試（Test Plan 文件）
5. 部署與驗收（Deploy、Acceptance Tests 文件）
6. 問題追蹤與修正（Known Issues 文件）

各階段皆有對應文件於 docs/ 目錄，並以里程碑方式追蹤進度。

## 任務追蹤 (Task Tracking)
所有任務均於 Jira 或 GitHub Issues 進行追蹤，主要任務類型包含：
- CSV 解析器開發
- Hash Index 實作
- 查詢語法與執行引擎
- 單元測試與壓力測試
- 文件撰寫與維護

每項任務皆指派負責人，並定期檢視進度與調整優先順序。