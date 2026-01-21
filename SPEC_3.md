在既有專案做以下修改

1. 建立一個新的 mcp server，參考後端，提供以下功能：
    - 新增書籍
    - 刪除書籍
    - 修改評價
    - 修改閱讀狀態
    - 列出書籍
2. 建立一個新的 Agent，註冊 mcp server 的工具
3. 在UI介面新增一個對話視窗，用Agent來與使用者互動
    - 視窗尺寸需放大
    - 支援重置對話功能
    - Agent 操作完成後需自動更新頁面列表
4. 使用envs/.env的設定檔，設定azure openai api key
5. 使用 docker compose 來管理所有開發套件

