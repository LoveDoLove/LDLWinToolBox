AI 長期記憶與專案約定 (AI Long-Term Memory & Project Conventions)

本文件是本倉庫 AI 代理人的「長期記憶與專案約定中心」。每一次與 AI 開始新對話時，AI 必須首先讀取本檔案與 AGENTS.md，以恢復對當前專案、技術棧、用戶偏好與持久約定的全面認知。

1. 專案基礎設定 (Project Context)

本節記錄當前專案的根本設定，請根據實際情況進行動態更新：

應用名稱 (App Name): LDL Windows ToolBox

資料庫 (App Database): 無（使用 JSON 設定檔儲存於 config/exclusions.json）

前端技術棧 (Frontend): ANSI Terminal Menu / Console（Python，依賴標準函式庫與方塊繪製字元）

後端技術棧 (Backend): Python 3.11+（僅使用標準函式庫，透過 subprocess 呼叫系統指令）

主權部署環境 (Deployment): GitHub Releases（PyInstaller 打包為單一 .exe）

2. 使用者偏好與互動慣例 (User Preferences)

溝通語言：預設使用 繁體中文 (Traditional Chinese) 進行所有對話、架構解釋與日誌記錄（除程式碼註解、變數命名與技術文檔採用英文）。

主要語言：Python（此專案）；遵循 pyproject.toml 中 Ruff 設定的程式碼風格。

指令紀律：嚴格遵循 RTK.md 規範，使用 rtk cmd /c ... 前綴執行 Windows 指令。僅在 Python 或原生工具無法達成時，才使用 PowerShell 單行指令。

程式碼風格：
- 追求極簡與健壯性，嚴禁過度設計。
- 優先使用 Python 標準函式庫，不引入外部依賴。
- 外科手術式變更：只修改目標區域，不重構無關的程式碼。
- 必須符合內置技能包 karpathy-guidelines 的編碼行為準則。

管理員行為：
- 自動偵測管理員權限；若無管理員權限則以唯讀模式執行。
- 必要時以 UAC 重新啟動（透過 shell.Run 提升權限）。

確認機制 (HITL)：所有破壞性寫入、長時間執行作業、遠端執行或涉及暫存檔目錄的操作，AI 必須暫停並明確徵求使用者 Y/N 批准。

日誌：時間戳結構化日誌寫入 logs/LDLWinToolBox_yyMMddHHmmss.log，主控台保持簡潔輸出。

技能包：必須從公開 GitHub 開源 Skills 倉庫克隆，嚴禁在本倉庫中自行手動編寫技能包。

檔案保留：不刪除舊有的決定、歷史記錄或備份檔案，除非使用者明確要求。

3. 記憶同步與更新協議 (Memory Sync Protocol)

為了確保 AI 的記憶在跨對話中永不丟失且持續演進，AI 助手必須遵循以下同步機制：

3.1 每日日誌機制 (Daily Logs YYYY-MM-DD.md)

每次對話結束前，AI 必須將當前的關鍵決策、面臨的問題與下一步計劃，摘要寫入 memory/YYYY-MM-DD.md（以當前日期命名）。

日誌格式標準：

# 每日工作日誌: YYYY-MM-DD
* **今日進度**: [簡述完成了哪些功能/修復了哪些 Bug]
* **關鍵決策**: [例如切換了某個 API、更新了某個 Schema]
* **遭遇阻礙**: [遇到的技術難題與解決路徑]
* **明日計劃**: [待續的具體工作事項]


3.2 任務追蹤機制 (tasks.md)

所有的跨對話待辦事項必須維護在 memory/tasks.md 中。

任務分為三個看板狀態：[ ] Backlog（待辦）、[>] In Progress（進行中）、[x] Completed（已完成）。

當 AI 助手完成一項任務時，必須同步更新 memory/tasks.md，並在日誌中註記。

4. 持久技術約定 (Persistent Rules)

安全優先原則：所有新開發的端點（Endpoints）或微服務，必須在核心邏輯外圍包裹安全認證層，貫徹 AGENTS.md 中的「受控副官防禦」。

零退化 CI/CD 承諾：凡是有新的重大業務邏輯變更，必須同步在 tests/ 下建立對應的斷言測試，以利後續自動化品質飛輪（AgentOps）的集成。

技能包（Agent Skills）優先：解決特定領域問題時（例如：SEO 審計、性能優化、程式碼重構），先檢索本地 .agents/skills/，優先調用已有技能。
