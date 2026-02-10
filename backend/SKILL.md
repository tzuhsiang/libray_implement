---
name: libriflow_manager
description: 圖書管理系統後端，支援書籍的新增、查詢、修改與刪除。
---

# LibriFlow Manager Skill

這是一個基於 FastMCP 實作的圖書管理工具。

## 功能介紹
你可以使用此 Skill 來執行下列操作：

1. **列出書籍** (`list_books`)：檢視目前的藏書清單。
2. **新增書籍** (`add_book`)：將新書加入資料庫。
3. **修改狀態** (`update_book_status`)：更新書籍的閱讀狀態（unread, reading, finished）。
4. **修改評分** (`update_book_rating`)：對書籍進行 0-5 分的評分。
5. **刪除書籍** (`delete_book`)：從資料庫中移除特定的書籍。

## 使用方式
請直接告知助理你想執行的動作，例如：
- 「幫我列出最近的 10 本書。」
- 「新增一本書，書名是《三體》，作者是劉慈欣。」
- 「把 ID 為 5 的書狀態改成『已讀』。」

## 檔案說明
- `mcp_server.py`: MCP Server 的核心實作。
- `agent.py`: 整合 Pydantic AI 的代理人實作。
- `models.py` & `schemas.py`: 資料模型定義。
