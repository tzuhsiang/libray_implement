專案開發規格書：LibriFlow 個人圖書管理系統
目標：建立一個包含 FastAPI 後端、Vue.js 3 前端及 PostgreSQL 資料庫的全端應用，並使用 Docker Compose 進行容器化部署。

1. 專案目錄結構
請依照以下結構建立專案，根目錄名稱為 libray_implement：

Plaintext

libray_implement/
├── backend/
│   ├── main.py              # FastAPI 應用主入口與路由
│   ├── models.py            # SQLAlchemy 資料庫模型
│   ├── schemas.py           # Pydantic 資料驗證模型
│   ├── database.py          # 資料庫連線配置 (SQLAlchemy)
│   ├── crud.py              # 資料庫增刪查改邏輯
│   ├── requirements.txt     # Python 套件清單
│   └── Dockerfile           # 後端映像檔構建檔
├── frontend/
│   ├── src/
│   │   ├── components/      # Vue 組件 (BookList, BookForm)
│   │   ├── App.vue          # 主頁面
│   │   └── main.js          # Vue 入口與 Axios 配置
│   ├── package.json
│   ├── index.html
│   ├── vite.config.js
│   └── Dockerfile           # 前端映像檔構建檔
├── envs/
│   ├── .env.example         # 環境變數範例檔
│   └── .env                 # 環境變數設定檔（不納入版控）
└── docker-compose.yml       # 多容器編排定義檔

2. 技術規格詳細定義

A. 後端 (FastAPI)
語言與框架：Python 3.12+, FastAPI。
資料庫工具：SQLAlchemy ORM。

功能需求：

實作 CORS 中介軟體，允許來自 http://localhost:5173 (Vue) 的請求。
API 節點：
GET /books：回傳所有書籍清單。
POST /books：新增書籍（欄位：title, author, status, rating）。
PUT /books/{id}：更新書籍狀態或評分。
DELETE /books/{id}：刪除書籍。
自動文件：確保 /docs 能夠正常顯示 Swagger UI。

B. 前端 (Vue 3 + Vite)
框架：Vue 3 (Composition API)。
樣式：Tailwind CSS。

功能需求：
BookList 組件：以卡片形式展示書籍，包含標題、作者、星星評分。
BookForm 組件：一個簡單的表單，用於輸入新書資訊。
狀態管理：使用 Axios 與後端 API 通訊。
響應式設計：確保在手機與電腦版皆可正常顯示。

C. 資料庫與部署 (Docker)
資料庫：PostgreSQL 15。

Docker Compose 配置：
db 服務：設定環境變數 POSTGRES_USER、POSTGRES_PASSWORD。
backend 服務：依賴 db，開放 8000 埠。
frontend 服務：開放 5173 埠，使用 Vite 的開發伺服器模式。
網路設定：三個服務必須在同一個 Docker Network 中。


3. 資料庫 Schema 定義欄位

欄位名	類型	 約束
id	    Integer	Primary Key, Autoincrement
title	String	Not Null
author	String	Not Null
status	String	Default: 'unread' (選項: unread, reading, finished)
rating	Integer	Min: 1, Max: 5, Default: 0







